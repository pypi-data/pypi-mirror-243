import importlib
import importlib.util
import json
import logging
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Optional

import click

from .build_config import get_build_config_for_stage
from .controller import controller


@click.group()
@click.option("-d", "--debug", help="Turn on debug logs", is_flag=True, default=False)
def cli(debug: bool):
    """
    async-lambda CLI. For building async-lambda applications.
    """
    if debug:
        logging.basicConfig(level=logging.INFO)


def import_module(module_name: str):
    project_dir = os.getcwd()
    vendor_dir = os.path.join(project_dir, "vendor")
    if os.path.exists(vendor_dir) and os.path.isdir(vendor_dir):
        sys.path.insert(0, vendor_dir)
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    importlib.import_module(module_name)


@cli.command()
@click.argument("module")
@click.option("-s", "--stage", help="The stage to build the app for.")
@click.option(
    "-o",
    "--output",
    default="template.json",
    help="The name of the file for the output template.",
)
def build(module: str, output: str, stage: Optional[str] = None):
    """
    Builds/generates the SAM template for the given module.
    """
    dir = Path.cwd()
    config = {}
    config_file = dir.joinpath(".async_lambda/config.json")
    if config_file.exists():
        config = json.loads(config_file.read_bytes())
    build_config = get_build_config_for_stage(config, stage=stage)
    os.environ.update(build_config.environment_variables)
    os.environ["ASYNC_LAMBDA_BUILD_MODE"] = "1"
    click.echo(f"Importing {module} module...")
    import_module(module)

    click.echo("Generating SAM template...")

    with open(os.path.join(os.getcwd(), output), "w") as template_file:
        template_file.write(
            json.dumps(
                controller.generate_sam_template(module, config, stage=stage), indent=2
            )
        )

    if os.path.exists(".async_lambda/build"):
        shutil.rmtree(".async_lambda/build")
    os.makedirs(".async_lambda/build/packages", exist_ok=True)

    if dir.joinpath("requirements.txt").exists():
        click.echo("Installing dependencies (requirements.txt) in build folder...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
                "--target",
                ".async_lambda/build/packages",
                "--upgrade",
            ]
        )

    click.echo("Bundling build zip file...")
    zip_file_name = ".async_lambda/build/deployment.zip"
    with zipfile.ZipFile(zip_file_name, "w") as z:
        entrypoint = dir.joinpath(f"{module}.py")
        z.write(entrypoint, entrypoint.relative_to(dir))

        for entry in dir.rglob("src/*"):
            z.write(entry, entry.relative_to(dir))

        packages_dir = dir.joinpath(".async_lambda", "build", "packages")
        for entry in packages_dir.rglob("*"):
            if entry.match("*__pycache__*"):
                continue
            z.write(entry, entry.relative_to(packages_dir))

        app_vendor_dir = dir.joinpath("vendor")
        for entry in app_vendor_dir.rglob("*"):
            z.write(entry, entry.relative_to(app_vendor_dir))

    click.echo(f"Created zip bundle {zip_file_name}")


if __name__ == "__main__":
    cli()
