"""
command line interface
"""
from argparse import ArgumentParser
from importlib.metadata import version
import json
import os
import re
import requests
from typing import Any, Dict, cast

from cookiecutter.main import cookiecutter

from seaplane.apps.build import read_project_file, validate_project
import seaplane.run_load_dotenv as denv
from seaplane.sdk_internal_utils.http import headers


class CliError(Exception):
    pass


def get_project() -> Dict[str, Any]:
    """
    Reads pyproject.toml
    """
    validate_project()
    return read_project_file()


def cli_deploy(task: str) -> None:
    """
    Deploys an app or task
    """
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} deploy {task}")


def cli_destroy() -> None:
    """
    Destroys an app (deletes streams and flows)
    """
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} destroy")


def cli_build() -> None:
    """
    Builds an app (writes build/schema.json)
    """
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} build")


def cli_status() -> None:
    """
    Provides status of an app's resources
    """
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} status")


def get_token(fd_url: str) -> str:
    """
    Gets a token from Flightdeck
    """
    # Try to get the API key from .env
    api_key = os.environ.get("SEAPLANE_API_KEY", "None")
    if denv.loaded is False or api_key == "None":
        print("Set your API key in .env")
        exit()

    response = requests.post(fd_url, json={}, headers=headers(api_key))
    if response.ok:
        payload = cast(Dict[str, str], response.json())
    else:
        error_body = response.text
        print(f"Bad Access token request code {response.status_code}, error {error_body}")
        exit()
    return payload["token"]


def cli_request(data: str) -> None:
    """
    Performs an endpoint request, writes and prints the request_id
    """
    if data[0] == "@":
        try:
            data_bytes = open(data[1:], "rb").read()
        except Exception:
            print("Cannot load data file.")
            exit()
    else:
        data_bytes = data.encode()

    # Load schema file
    try:
        schema_file = open(os.path.join("build", "schema.json"), "r")
        schema = json.load(schema_file)
    except Exception:
        print("Cannot load build schema. Try moving to the directory where you deploy your app.")
        exit()

    # Get a token
    fd_url = schema["identity_endpoint"] + "/token"
    token = get_token(fd_url)

    # Make the request
    for app in schema["apps"]:
        app_id = schema["apps"][app]["id"]
    carrier_endpoint = schema["carrier_endpoint"]
    url = f"{carrier_endpoint}/endpoints/{app_id}/request"
    bearer = {"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    resp = requests.post(url, headers=bearer, data=data_bytes)
    request_id = json.loads(resp.content)["request_id"]

    # save the request_id to a file
    with open(".request_id", "a") as f:
        f.write(f"{request_id}\n")
    print(f"\nrequest_id: {request_id}")


def cli_response(request_id: str) -> None:
    """
    Gets an archive response from the endpoint
    """
    # TODO: Could (with arg?) show a list of the last 5-10 ids to choose
    if request_id == "":
        try:
            with open(".request_id", "r") as f:
                request_id = f.readlines()[-1].strip("\n")
        except Exception:
            print("No request_id provided as argument or in file")

    # Load schema file
    try:
        schema_file = open(os.path.join("build", "schema.json"), "r")
        schema = json.load(schema_file)
    except Exception:
        print("Cannot load build schema. Try moving to the directory where you deploy your app.")
        exit()

    # Get a token
    fd_url = schema["identity_endpoint"] + "/token"
    token = get_token(fd_url)

    # Make the request
    for app in schema["apps"]:
        app_id = schema["apps"][app]["id"]
    carrier_endpoint = schema["carrier_endpoint"]
    url = f"{carrier_endpoint}/endpoints/{app_id}/response/{request_id}/archive"
    bearer = {"Authorization": f"Bearer {token}", "accept": "application/octet-stream"}
    resp = requests.get(url, headers=bearer, params={"pattern": ".>", "format": "json_array"})
    print(f"\nResponse archive for request_id {request_id}:")
    print(resp.content)


def init(project_name: str) -> None:
    """
    Initializes a project using a template
    """
    cookiecutter_template = "https://github.com/seaplane-io/seaplane-app-python-template.git"
    project_directory = "."

    if not project_name.isidentifier():
        suggestion = re.sub("[^A-Za-z0-9_]", "", project_name)
        raise CliError(f'can\'t make a new project named "{project_name}". Try "{suggestion}"')

    extra_context = {"project_slug": project_name, "seaplane_version": version("seaplane")}

    cookiecutter(
        cookiecutter_template,
        output_dir=project_directory,
        no_input=True,  # Disable any interactive prompts
        extra_context=extra_context,
    )

    print(f"🛩️  {project_name} project generated successfully!")


def main() -> None:
    parser = ArgumentParser(prog="seaplane", description="Seaplane Apps command line interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    subparsers.add_parser("build", help="Build command")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy command")
    deploy_parser.add_argument(
        "--task",
        type=str,
        help="seaplane deploy which can include a TASK_ID as a parameter to deploy an individual TASK",  # noqa
    )

    # Destroy command
    subparsers.add_parser("destroy", help="Remove your App and associated tasks")

    # Init command
    init_parser = subparsers.add_parser("init", help="Init command")
    init_parser.add_argument("app", help="Seaplane Apps name")

    # Status command
    subparsers.add_parser("status", help="Status of your app and resources")

    # Endpoints commands
    req_parser = subparsers.add_parser("request", help="Send data to the request endpoint")
    req_parser.add_argument(
        "--data", "-d", type=str, help="Request body, @ to load a file, @- for stdin"
    )
    resp_parser = subparsers.add_parser("response", help="Get data from the response endpoint")
    resp_parser.add_argument("--request_id", "-r", type=str, help="Request ID")

    # Version argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=version("seaplane")),
    )

    args = parser.parse_args()

    if args.command == "build":
        cli_build()

    elif args.command == "deploy":
        task = ""
        if args.task:
            task = args.task

        cli_deploy(task)

    elif args.command == "destroy":
        cli_destroy()

    elif args.command == "init":
        init(args.app)

    elif args.command == "status":
        cli_status()

    elif args.command == "request":
        cli_request(args.data)

    elif args.command == "response":
        request_id = ""
        if args.request_id:
            request_id = args.request_id
        cli_response(request_id)

    else:
        parser.print_help()

    exit(0)


if __name__ == "__main__":
    main()
