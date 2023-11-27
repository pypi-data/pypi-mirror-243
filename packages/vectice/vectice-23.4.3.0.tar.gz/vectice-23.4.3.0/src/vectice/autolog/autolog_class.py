from __future__ import annotations

import json
import logging
import os
import random
import re
import string
import tempfile
from ast import literal_eval
from enum import Enum
from functools import reduce
from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, TypedDict, TypeVar

from vectice.models.resource.metadata.db_metadata import TableType
from vectice.services.phase_service import PhaseService


class ModelLibrary(Enum):
    """Enumeration that defines what the model library."""

    SKLEARN = "SKLEARN"
    LIGHTGBM = "LIGHTGBM"
    CATBOOST = "CATBOOST"
    NONE = "NONE"


if TYPE_CHECKING:
    import matplotlib.pyplot as plt
    from catboost.core import CatBoost
    from lightgbm.basic import Booster
    from matplotlib.axes import SubplotBase
    from matplotlib.figure import Figure
    from pandas import DataFrame
    from plotly.graph_objs._figure import Figure as PltFigure
    from pyspark.sql import DataFrame as SparkDF
    from sklearn.base import BaseEstimator

    from vectice.models import Iteration, Phase

    ModelTypes = TypeVar("ModelTypes", BaseEstimator, Booster, CatBoost)
    TModel = TypedDict("TModel", {"variable": str, "model": ModelTypes, "library": ModelLibrary})
    DataframeTypes = TypeVar("DataframeTypes", SparkDF, DataFrame)
    TDataset = TypedDict("TDataset", {"variable": str, "dataframe": DataframeTypes, "type": TableType})


try:
    import ipynbname
    from IPython.core.interactiveshell import InteractiveShell
    from nbformat import NO_CONVERT, read
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "To use autolog, please install extra dependencies from vectice package using '%pip install vectice[autolog]'"
    ) from None

is_plotly = False
is_matplotlib = False
if find_spec("plotly") is not None:
    from plotly.graph_objs._figure import Figure as PltFigure

    is_plotly = True

if find_spec("matplotlib") is not None:
    import matplotlib.pyplot as plt
    from matplotlib.axes import SubplotBase
    from matplotlib.figure import Figure

    is_matplotlib = True

_logger = logging.getLogger(__name__)


####### Autolog logic
class Autolog:
    def __init__(self, phase: Phase | None, ipy: InteractiveShell, is_notebook: bool, create: bool = True):
        if phase is None:
            raise ValueError("Login")

        if create is True:
            iteration = phase.create_iteration()
        else:
            iteration = PhaseService(
                phase._client  # pyright: ignore[reportPrivateUsage]
            ).get_active_iteration_or_create(phase)

        self._ip = ipy
        self._local_vars = self._ip.user_global_ns
        self._cell_content = self._get_notebook_cell_content() if is_notebook is True else self._get_cell_content()
        self._vectice_data = (
            {variable: self._local_vars[variable] for variable in self._local_vars.keys()}
            if is_notebook is True
            else self._get_variable_matches(self._local_vars)
        )
        self._failed_assets = []

        # Get back objects to log
        assets = self._get_assets()
        model_metrics = self._get_model_metrics()
        graph = self._get_graph()

        # Log objects
        self._log_assets(iteration, assets, model_metrics)

        # Find weird the differences between the notebook log and the cell log
        # Temp fix, notebook getting the graphs again breaks them (blank graph)
        # Only get back one graph ?? Why ?
        # Just for demo, one graph is temporary, we can add logic for multiple
        # Graphs aren't stable so you get blank graphs, need to test multiple graphs
        if is_notebook is True:
            # TODO fix reuse, blank graph with autolog notebook. Temp fix implemented
            graphs = self._get_notebook_graphs()
            for graph in graphs:
                try:
                    iteration.log(graph)
                except Exception:
                    self._failed_assets.append(graph)
        else:
            if graph:
                self._log_graph(graph, iteration)

        _logger.warning(
            f"The following assets failed to log:\n{', '.join(self._failed_assets)}"
        ) if self._failed_assets else None

    def _get_variable_matches(self, local_vars: dict[str, Any]) -> dict[Any, Any]:
        # TODO clean this up
        matches = re.findall(r"(.*?) =", self._cell_content)
        vectice_data = {}
        for variable in matches:
            try:
                vectice_data[variable] = local_vars[variable]
            except KeyError:
                pass
        return vectice_data

    def _get_notebook_path(self) -> str:
        try:
            nb_path = ipynbname.path()
            nb_full_path = os.path.join(os.getcwd(), nb_path.name)
        except FileNotFoundError:
            nb_full_path = None
        # VS Code notebook path
        nb_full_path = self._local_vars.get("__vsc_ipynb_file__") if not nb_full_path else nb_full_path

        if not nb_full_path:
            raise ValueError("The notebook file was not found.")
        return nb_full_path

    def _get_notebook_cell_content(self) -> str:
        nb_full_path = self._get_notebook_path()

        try:
            with open(nb_full_path) as fp:
                notebook = read(fp, NO_CONVERT)
            cells = notebook["cells"]  # pyright: ignore[reportGeneralTypeIssues]
            code_cells = [cell for cell in cells if cell["cell_type"] == "code"]  # ignore: type
            return "\n".join([cell["source"] for cell in code_cells])
        except FileNotFoundError:
            # Try to get collab notebook content
            return self._get_collab_notebook_cell_content()

    def _get_collab_notebook_cell_content(self) -> str:
        from vectice.utils.ipython_hook import auth_drive, get_current_collab_notebook

        drive = auth_drive()
        if not drive:
            raise ValueError("GoogleDrive failed to authenticate.")
        _, file_id = get_current_collab_notebook()
        collab_drive_file = drive.CreateFile({"id": file_id})
        collab_notebook = json.loads(collab_drive_file.GetContentString())
        cells = collab_notebook["cells"]
        code_cells = [
            cell for cell in cells if cell["cell_type"] == "code" and len(cell["source"]) >= 1
        ]  # ignore: type
        return_cells = []
        for cell in code_cells:
            if cell.get("source") and len(cell["source"][0]) >= 1:
                # add newline to last code line in array
                cell["source"][-1] = cell["source"][-1] + "\n"
                # flatten the whole cell and keep newline breaks
                cell_source = "".join(cell["source"])
                # add to return
                return_cells.append(cell_source)
        # flatten the list to match what's expected
        return "".join(return_cells)

    def _get_cell_content(self) -> str:
        """Used by autolog cell to get the content of the cell. This is used to parse for variables."""
        cell_content = self._ip.get_parent()["content"]["code"]  # pyright: ignore[reportGeneralTypeIssues]
        if cell_content is None:
            raise ValueError("Failed to get cell content.")
        return cell_content

    def _get_sklearn_api_model(self, model: TModel):
        # xgboost relies on BaseEstimator
        # lightgbm has Booster and sklearn API which uses BaseEstimator
        try:
            from sklearn.base import is_classifier, is_regressor

            if is_regressor(model["model"]) or is_classifier(model["model"]):
                try:
                    # TODO fix regex picking up classes
                    # Ignore Initialized variables e.g LogisticRegression Class
                    model["model"].get_params()  # pyright: ignore[reportGeneralTypeIssues]
                    return model
                except Exception:
                    pass
        except ImportError:
            pass

    def _get_assets(self) -> list[TModel | TDataset]:
        is_pandas = find_spec("pandas") is not None
        is_pyspark = find_spec("pyspark") is not None
        is_lgbm = find_spec("lightgbm") is not None
        is_sklearn = find_spec("sklearn") is not None
        is_catboost = find_spec("catboost") is not None

        assets = []
        for key in self._vectice_data.keys():
            # skip cell inputs/outputs
            if key.startswith("_"):
                continue
            asset = self._vectice_data[key]
            if is_pandas:
                from pandas import DataFrame

                if isinstance(asset, DataFrame):
                    assets.append({"variable": key, "dataframe": asset, "type": TableType.PANDAS})
            if is_pyspark:
                from pyspark.sql import DataFrame as SparkDF

                if isinstance(asset, SparkDF):
                    assets.append({"variable": key, "dataframe": asset, "type": TableType.SPARK})

            model: TModel = {"variable": key, "model": self._vectice_data[key], "library": ModelLibrary.NONE}
            if is_lgbm:
                from lightgbm.basic import Booster

                if isinstance(model["model"], Booster):
                    model["library"] = ModelLibrary.LIGHTGBM
                    assets.append(model)
            if is_catboost:
                from catboost.core import CatBoost

                if isinstance(model["model"], CatBoost):
                    model["library"] = ModelLibrary.CATBOOST
                    assets.append(model)
            elif is_sklearn:
                sklearn_model = self._get_sklearn_api_model(model)

                if sklearn_model is not None:
                    model["library"] = ModelLibrary.SKLEARN
                    assets.append(sklearn_model)

        return assets

    def _get_model_metrics(self) -> dict[str, Any]:
        # TODO mix of models ?
        if not self._cell_content:
            return {}

        metrics = self._get_regression_metrics() or self._get_classification_metrics()
        # Temporary fix for additional metrics used with regression or classification
        other_metrics = self._get_other_metrics()
        metrics += other_metrics
        return reduce(
            lambda identified_metrics, key: {**identified_metrics, key: self._vectice_data[key]}
            if key in metrics
            else identified_metrics,
            self._vectice_data.keys(),
            {},
        )

    def _get_regression_metrics(self):
        from sklearn.metrics import _regression  # pyright: ignore[reportPrivateUsage]

        return reduce(self._get_metric, dir(_regression), [])

    def _get_classification_metrics(self):
        from sklearn.metrics import _classification  # pyright: ignore[reportPrivateUsage]

        return reduce(self._get_metric, dir(_classification), [])

    def _get_other_metrics(self):
        from sklearn.metrics import (
            _ranking,  # pyright: ignore[reportPrivateUsage]
            _scorer,  # pyright: ignore[reportPrivateUsage]
            cluster,  # pyright: ignore[reportPrivateUsage]
        )

        all_metrics = dir(_ranking) + dir(_scorer) + dir(cluster)
        return reduce(self._get_metric, all_metrics, [])

    def _get_metric(self, metrics: list[Any], func: str):
        # TODO regex working but should be tested more
        metric = re.findall(rf"(.*?) = {func}", self._cell_content)
        return [*metrics, *metric] if metric else metrics

    def _get_graph(self) -> Figure | SubplotBase | PltFigure | None:
        # catch tuple naming fig, axes plt.subplots
        check_plt = re.findall(r"(.*?) = plt.subplots", self._cell_content)
        if check_plt:
            variable = check_plt[0].split(",")[0] if len(check_plt[0].split(",")) > 1 else None
            if variable:
                self._vectice_data[variable] = self._local_vars[variable]

        plot_types = ()

        if is_matplotlib:
            plot_types += (
                Figure,
                SubplotBase,
            )

        if is_plotly:
            plot_types += (PltFigure,)

        if not is_plotly and not is_matplotlib:
            return None

        # Only check cell for graphs, notebook graphs are captured differently
        for key in self._vectice_data:
            var = self._vectice_data[key]
            if isinstance(var, plot_types) or (is_matplotlib and plt is var):
                return var

    def _get_lightgbm_info(self, model: Booster) -> tuple[str, dict] | tuple[None, None]:
        try:
            params = {
                key: value
                for key, value in model._get_loaded_param().items()  # pyright: ignore[reportPrivateUsage]
                if value is not None
            }
            return "lightgbm", params
        except AttributeError:
            return None, None

    def _get_model_library(self, model: ModelTypes):
        if "xgboost" in str(model.__class__):
            return "xgboost"
        if "lightgbm" in str(model.__class__):
            return "lightgbm"
        return "sklearn"

    def _get_sklearn_or_xgboost_or_lgbm_info(self, model: BaseEstimator) -> tuple[str, dict] | tuple[None, None]:
        try:
            library = self._get_model_library(model)
            params = {key: value for key, value in model.get_params().items() if value is not None}
            return library, params
        except AttributeError:
            return None, None

    def _log_assets(
        self,
        iteration: Iteration,
        assets: list[TModel | TDataset],
        model_metrics: dict[str, Any] | None = None,
    ):
        len_models = len(list(filter(lambda asset: True if "model" in asset else False, assets)))
        if len_models >= 2:
            logging.warning("Metrics aren't captured for multiple models currently.")
            model_metrics = None
        for asset in assets:
            try:
                if "model" in asset:
                    self._log_model(asset, iteration, model_metrics)
                else:
                    self._log_dataset(asset, iteration)
            except Exception:
                self._failed_assets.append(asset["variable"])

    def _get_catboost_info(self, model: CatBoost) -> tuple[str, dict] | tuple[None, None]:
        try:
            params = {key: value for key, value in model.get_all_params().items() if value is not None}
            return "catboost", params
        except AttributeError:
            return None, None

    def _get_model_params(self, model: TModel) -> tuple[str, dict] | tuple[None, None]:
        if model["library"] is ModelLibrary.SKLEARN:
            return self._get_sklearn_or_xgboost_or_lgbm_info(model["model"])  # pyright: ignore[reportGeneralTypeIssues]
        if model["library"] is ModelLibrary.LIGHTGBM:
            return self._get_lightgbm_info(model["model"])  # pyright: ignore[reportGeneralTypeIssues]
        if model["library"] is ModelLibrary.CATBOOST:
            return self._get_catboost_info(model["model"])  # pyright: ignore[reportGeneralTypeIssues]
        return None, None

    def _log_model(self, model: TModel, iteration: Iteration, model_metrics: dict[str, Any] | None = None):
        from vectice import Model

        library, params = self._get_model_params(model)

        algorithm = str(model["model"].__class__).split(".")[-1]
        algorithm = algorithm.replace("'>", "")
        model_name = f"{iteration.phase.id}-{model['variable']}"

        iteration.log(
            Model(
                library=library,
                technique=algorithm,
                metrics=model_metrics,
                properties=params,
                name=model_name,
                predictor=model["model"],
            )
        )

    def _log_dataset(self, dataset: TDataset, iteration: Iteration) -> None:
        from vectice import Dataset, DatasetType, FileResource, NoResource

        resource = self._get_dataset_resource(dataset)
        dataset_name = f"{iteration.phase.id}-{dataset['variable']}"
        no_resource_dataset = Dataset(
            type=DatasetType.UNKNOWN,
            resource=NoResource(
                dataframes=dataset["dataframe"],
                origin="DATAFRAME",
                type=dataset["type"],
            ),
            name=dataset_name,
        )
        if resource:
            # TODO Dataset type ?
            vec_dataset = Dataset(
                type=DatasetType.UNKNOWN,
                resource=FileResource(
                    paths=resource,
                    dataframes=dataset["dataframe"],
                ),
                name=dataset_name,
            )
        else:
            vec_dataset = no_resource_dataset
        try:
            iteration.log(vec_dataset)
        except FileNotFoundError:
            iteration.log(no_resource_dataset)

    def _get_dataset_resource(self, dataset: TDataset) -> str | None:
        import re

        if not self._cell_content:
            return None
        try:
            # Avoid getting stray dataset with autolog.notebook()
            match = re.findall(rf"(?<={dataset['variable']} = pd.read_csv\().*[^,)\n]", self._cell_content)
            if len(match) < 1:
                return None
            # TODO update regex
            # check if read csv has comma dominated arguments
            return literal_eval(match[0].split(",")[0]) if match[0].find(",") else literal_eval(match[0])
        except TypeError:
            return None

    def _log_graph(self, graph: PltFigure | SubplotBase | Figure, iteration: Iteration):
        # TODO fix reuse, blank graph with autolog notebook
        temp_dir = tempfile.mkdtemp()
        file_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        temp_file_path = rf"{temp_dir}\{file_name}.png"
        try:
            if is_plotly and isinstance(graph, PltFigure):
                graph.write_image(temp_file_path)
                iteration.log(temp_file_path)
            else:
                if isinstance(graph, SubplotBase):
                    graph.figure.savefig(temp_file_path)  # pyright: ignore[reportGeneralTypeIssues]
                if isinstance(graph, Figure):
                    graph.savefig(temp_file_path)
                elif graph is plt:
                    graph.savefig(temp_file_path)  # pyright: ignore[reportGeneralTypeIssues]
                iteration.log(temp_file_path)
        except Exception:
            self._failed_assets.append(temp_file_path)

    def _get_notebook_graphs(self) -> list[str]:
        graphs = []
        # seaborn and matplotlib support
        graphs += re.findall(r"(?<=plt.savefig\().*[^\)\n]", self._cell_content)
        # plotly support
        graphs += re.findall(r"(?<=.write_image\().*[^\)\n]", self._cell_content)
        return [literal_eval(graph) for graph in graphs]
