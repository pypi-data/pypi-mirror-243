# This captures the code called, we then use regex to identify the variables in locals. The variables found can then be logged to vectice.
"""Auto-Logging assets with Vectice.

NOTE: **This feature is currently in Beta and is subject to change. To activate this feature please contact your sales representative.**

------------
The enhanced auto-logging feature in Vectice allows for seamless documentation and management of your data science projects. Please note the following details about this beta feature.

NOTE: **This feature is designed to work specifically with Jupyter notebooks.**

1. **Installation:**
    To enable the auto-logging feature, install the additional dependencies using the following command:

    ```bash
    pip install vectice[autolog]
    ```
2. **Supported libraries and environment:**
    Vectice automatically identifies and log assets encapsulated within a specified list of supported libraries and environement mentioned below

NOTE: Supported libraries and environment
    - Dataframe: Pandas, Spark
    - Model: Scikit, Xgboost, Lightgbm, Catboost
    - Graphs: Matplotlib, Seaborn, Plotly
    - Environments: Vscode, colab, jupyter, vertex notebook
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell

    from vectice.models import Phase


class Login(TypedDict):
    phase: Phase | None


LOGIN: Login = {"phase": None}


# Setup vectice connection on phass
def config(api_token: str, phase: str, host: str | None = None) -> None:
    """Configures the autolog functionality within Vectice.

    The `config` method allows you to establish a connection to Vectice and specify the phase in which you want to autolog your work.

    ```python
    # Configure autolog
    from vectice import autolog
    autolog.config(
        api_token = 'your-api-key', # Paste your api key
        phase = 'PHA-XXX'           # Paste your Phase Id
    )
    ```

    Parameters:
            api_token: The api token provided inside your Vectice app (API key).
            phase: The ID of the phase in which you wish to autolog your work as an iteration.
            host: The backend host to which the client will connect. If not found, the default endpoint https://app.vectice.com is used.

    """
    import vectice
    from vectice.models.workspace import Workspace

    vec = vectice.connect(api_token=api_token, host=host)  # Paste your API token
    LOGIN["phase"] = vec.connection.phase(phase) if isinstance(vec, Workspace) else vec.phase(phase)
    vec._client.assert_feature_flag_or_raise("autolog")  # pyright: ignore[reportPrivateUsage]


# Log the whole notebook inside Vectice iteration
def notebook() -> None:
    """Automatically log all supported models, dataframes, and graphs from your notebook within the Vectice App as assets.

    NOTE: **Ensure that you have configured the autolog with your Vectice API token and the relevant phase ID before using this method.**

    ```python
                                   ...
    #Add this command at the end of notebook to log all the assets in memory
    autolog.notebook()
    ```

    NOTE: **Ensure that the required assets are in memory before calling this method.**

    NOTE: IMPORTANT INFORMATION
        - For autolog.notebook() only, ensure that GRAPHS are saved as files to be automatically captured in the documentation.
        - Vectice currently only detects sklearn metrics for association with models.
        - If there is ambiguity—where multiple models with different metrics exist—Vectice won't automatically associate them together. To link them, please ensure that each model and its respective metrics are placed in the same notebook cell.

    """
    from vectice.autolog.autolog_class import Autolog

    # TODO add notebook parsing of content
    Autolog(LOGIN["phase"], _check_if_notebook(), True)


# Log a cell inside Vectice iteration


def cell(create_new_iteration: bool = False):
    """Automatically logs all supported models, dataframes, and graphs from a specific notebook cell within the Vectice platform.

    This method facilitates the selective logging of assets within a particular notebook cell, allowing users to precisely choose the assets to log to Vectice with an optional control to log assets inside a new iteration.

    NOTE: **Ensure that you have configured the autolog with your Vectice API token and the relevant phase ID before using this method.**

    ```python
                                   ...
    #Add this command at the end of the desired cell to log all the cells assets
    autolog.cell()
    ```

    NOTE: **Place the command at the end of the desired cell to log all assets within that cell.**

    Parameters:
            create_new_iteration: If set to False, logging of assets will happen in the last updated iteration. Otherwise, it will create a new iteration for logging the cell's assets.

    """
    from vectice.autolog.autolog_class import Autolog

    Autolog(LOGIN["phase"], _check_if_notebook(), False, create_new_iteration)


def cell_vars(offset: int = 1) -> dict[str, Any] | None:
    # Not used currently but this gets the content of the entire notebook and parses for variables.
    import io
    from contextlib import redirect_stdout

    from IPython.core.getipython import get_ipython

    ipy = get_ipython()
    out = io.StringIO()
    if not ipy:
        return None
    with redirect_stdout(out):
        ipy.magic("history {0}".format(ipy.execution_count - offset))

    # process each line...
    x = out.getvalue().replace(" ", "").split("\n")
    x = [a.split("=")[0] for a in x if "=" in a]  # all of the variables in the cell
    g = globals()
    result = {k: g[k] for k in x if k in g}
    return result


def _check_if_notebook() -> InteractiveShell:
    from IPython.core.getipython import get_ipython

    ipython = get_ipython()

    if ipython is None:
        raise ValueError("Not a notebook.")
    return ipython
