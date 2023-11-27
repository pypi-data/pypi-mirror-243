from __future__ import annotations

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path, PurePath
from typing import Generator
from urllib.parse import unquote

import requests
from pydrive2.drive import GoogleDrive

from vectice.api.http_error import HttpError


def get_absolute_path() -> str:
    """Get the path for the directory walk to check if there's a .git and initialize the Repo object.

    Relates to 'drive.mount('/content/drive')' as '/content/' is part of the path and 'drive/' is
    required or the path will not be found.

    """
    filename, file_id = get_current_collab_notebook()
    path = str(get_collab_path(file_id=file_id, drive=None))
    try:
        path_formatting = path.split("/")
        path_formatting.pop()
        completed_path = "/".join(path_formatting)
        return f"drive/{completed_path}/{filename}"
    except ValueError:
        return str(path)


def get_current_collab_notebook():
    """Get the filename, file_id of this notebook."""
    jupyter_address = _get_collab_juptyer_server()
    jupyter_data = requests.get(f"http://{jupyter_address}/api/sessions").json()[0]
    filename = unquote(jupyter_data["name"])
    file_id = jupyter_data["path"].split("=")[1]
    return filename, file_id


def get_collab_path(file_id: int, drive: GoogleDrive | None = None) -> Path:
    """Use file_id to get the file path in Google Drive.

    NB needs to be mounted. User setup is conditional:

    from google.colab import drive
    drive.mount('/content/drive')
    """
    if drive is None:
        drive = auth_drive()
    if drive:
        file = drive.CreateFile({"id": file_id})
        name = file["title"]
        if file["parents"]:
            parent_id = file["parents"][0]["id"]
            return get_collab_path(parent_id, drive) / name
        else:
            return Path(name)
    raise ValueError("Google drive failed to authenticate.")


def _list_running_servers() -> Generator[dict, None, None]:
    """Iterate over the server info files of running notebook servers."""
    from jupyter_core.paths import jupyter_runtime_dir

    jupyter_runtime_dir = jupyter_runtime_dir()
    runtime_dir = Path(jupyter_runtime_dir)
    file_name = Path(f"{runtime_dir}\\{_most_recent_file(runtime_dir)[0]}")
    yield json.loads(file_name.read_bytes())


def _most_recent_file(directory_path: str | Path):
    """Get the jupyter server json file faster.

    Get the last modified file to get the currently active server.
    """
    server_most_recent_file = None
    server_most_recent_time = 0

    # kernel_most_recent_file = None
    kernel_most_recent_time = 0

    # iterate over the files in the directory using os.scandir
    for entry in os.scandir(directory_path):
        # Get the lastest modified server json
        if entry.is_file() and ("server" in entry.name and "json" in entry.name):
            # get the modification time of the file using entry.stat().st_mtime_ns
            server_mod_time = entry.stat().st_mtime_ns
            if server_mod_time > server_most_recent_time:
                # update the most recent file and its modification time
                server_most_recent_file = entry.name
                server_most_recent_time = server_mod_time
        # Get the lastest modified kernel json
        if entry.is_file() and "kernel" in entry.name:
            # get the modification time of the file using entry.stat().st_mtime_ns
            kernel_mod_time = entry.stat().st_mtime_ns
            if kernel_mod_time > kernel_most_recent_time:
                # update the most recent file and its modification time
                # kernel_most_recent_file = entry.name
                kernel_most_recent_time = kernel_mod_time

    return [server_most_recent_file]


def _get_kernel_id() -> str:
    """Returns the kernel ID of the ipykernel."""
    import ipykernel

    connection_file = Path(ipykernel.get_connection_file()).stem
    kernel_id = connection_file.split("-", 1)[1]
    return kernel_id


def _get_sessions(server: dict) -> dict:
    """Given a server, returns sessions, or HTTPError if access is denied.

    NOTE: Works only when either there is no security or there is token
    based security. An HTTPError is raised if unable to connect to a
    server.
    """
    query_str = ""
    token = server["token"]
    if token:
        query_str = f"?token={token}"
    host = "http://127.0.0.1:8888"
    url = f"/{host}api/sessions{query_str}"  # nosec
    with urllib.request.urlopen(url) as request:  # nosec
        if not (200 <= request.status_code < 300):
            raise HttpError(request.status_code, request.text, url, "GET", None)
        return json.load(request)  # nosec


def _find_notebook_path() -> tuple[dict | None, PurePath] | tuple[None, None]:  # pyright: ignore[reportUnusedFunction]
    from traitlets.config import MultipleInstanceError

    root = None
    file_path = None

    try:
        kernel_id = _get_kernel_id()
    except (MultipleInstanceError, RuntimeError):
        return None, None  # Could not determine
    server = None
    for server in _list_running_servers():
        root = server["root_dir"]
        try:
            sessions = _get_sessions(server)
            for sess in sessions:
                file_path = sess["notebook"]["path"]
                if sess["kernel"]["id"] == kernel_id:
                    return server, PurePath(sess["notebook"]["path"])  # nosec
        # There may be stale entries in the runtime directory
        except Exception:  # nosec
            pass  # nosec
    return server, PurePath(f"{root}\\{file_path}")


def auth_drive() -> GoogleDrive | None:
    """Authenticate Google Drive."""
    from google.colab import auth  # pyright: ignore[reportMissingImports]
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from oauth2client.client import GoogleCredentials
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive

    scopes = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
    drive = None
    if os.getenv("GOOGLE_DRIVE_TOKEN"):
        creds = Credentials.from_authorized_user_file(os.getenv("GOOGLE_DRIVE_TOKEN"), scopes)
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    elif os.getenv("GOOGLE_DRIVE_TOKEN") is None:
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)
    return drive


def _get_collab_juptyer_server() -> str | None:
    process = subprocess.Popen(
        "sudo lsof -i -P -n | grep LISTEN", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    jupyter_address = None
    if process.stdout is None:
        return jupyter_address
    for line in process.stdout.readlines():
        collab_ip = re.findall(r"jupyter-n.*?TCP(.*?)\(LISTEN\)", line.decode())
        if jupyter_address:
            break
        jupyter_address = collab_ip[0].strip() if len(collab_ip) >= 1 else None
    return jupyter_address


def _find_git_path(drive: GoogleDrive | None = None):  # pyright: ignore[reportUnusedFunction]
    """Find the git path relative to the google drive directory."""
    if drive is None:
        drive = auth_drive()
    if drive:
        file_list = drive.ListFile({"q": " title='.git' "}).GetList()
        return get_collab_path(file_list[0]["id"])
    raise ValueError("Google drive failed to authenticate.")
