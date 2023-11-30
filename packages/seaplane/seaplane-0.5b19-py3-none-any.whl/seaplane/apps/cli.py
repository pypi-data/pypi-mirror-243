"""
command line interface
"""
from argparse import ArgumentParser
from importlib.metadata import version
import os
import re
from typing import Any, Dict

from cookiecutter.main import cookiecutter

from seaplane.apps.build import read_project_file, validate_project


class CliError(Exception):
    pass


def get_project() -> Dict[str, Any]:
    validate_project()
    return read_project_file()


def cli_deploy(task: str) -> None:
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} deploy {task}")


def cli_destroy() -> None:
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} destroy")


def cli_build() -> None:
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} build")


def cli_status() -> None:
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main_script = project["tool"]["seaplane"]["main"]
    os.system(f"poetry run python {project_name}/{main_script} status")


def init(project_name: str) -> None:
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

    else:
        parser.print_help()

    exit(0)


if __name__ == "__main__":
    main()
