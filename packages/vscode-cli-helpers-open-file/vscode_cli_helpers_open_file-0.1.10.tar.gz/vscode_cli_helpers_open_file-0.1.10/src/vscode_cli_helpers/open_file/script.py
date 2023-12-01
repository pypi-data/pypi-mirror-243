#! /usr/bin/env python3

import logging
import platform
import subprocess
from pathlib import Path
from typing import Optional

import click

from vscode_cli_helpers.open_file.config import Config
from vscode_cli_helpers.open_file.exceptions import ConfigException
from vscode_cli_helpers.open_file.open_file import OpenFile


def edit_config_file(config: Config) -> None:
    """Edit the config file."""
    config_path = config.get_config_file()
    edit_file(config, config_path)


def edit_file(config: Config, file: Path) -> None:
    """Edit the config file."""
    cfg = config.config["Editor"]
    if platform.system() == "Linux":
        editor = cfg["Linux"]
        cmd = editor
        args = [str(file)]
    elif platform.system() == "Darwin":
        cmd = "open"
        editor = cfg["MacOS"]
        args = ["-a", editor, str(file)]
    elif platform.system() == "Windows":
        editor = cfg["Windows"]
        cmd = editor
        args = [str(file)]
    else:
        raise ConfigException(f"Unknown platform: {platform.system()}")
    logging.info(f"Running: {cmd} {args}")
    subprocess.Popen([cmd, *args], start_new_session=True)


def edit_template_file(config: Config, template: Optional[str]) -> None:
    """Edit the template file."""
    path = config.get_template_path(template)
    edit_file(config, path)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """``vscode-cli-helpers-open-file`` is a command line tool for opening new
    or existing files in VS Code and navigating to a specific line.
    """
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)


@main.command()
def edit_config() -> None:
    """``vscode-cli-helpers-open-file edit-config`` lets you edit the config file"""
    config = Config()
    edit_config_file(config)


@main.command()
@click.argument("template", type=str, required=False)
def edit_template(template: str) -> None:
    """``vscode-cli-helpers-open-file edit-template`` lets you edit the template file"""
    config = Config()
    edit_template_file(config, template)


@main.command()
@click.argument("path", type=str, required=False)
@click.option("--template", type=str, help="specify the template to use")
def open(path: Optional[str], template: Optional[str]) -> None:
    """``vscode-cli-helpers-open-file open`` lets you open a new
    or existing file in VS Code and navigating to a specific line number.
    You may consider creating a short alias for the sub commands you use most often, see
    :doc:`Creating an alias <alias>` for more information.

    If the ``--template`` option is not used, the file extension of ``PATH`` will be used
    to determine the template to use. If the :doc:`file extension <file_extension>` is not
    recognized, a default template will be used. For more information about specifying the
    default template, see :doc:`/template`.

    If the file exists, it will be opened in VS Code at line 1 or a specified line number.
    If the file does not exist, it will be created and the template will be written to the
    file before opening it in VS Code. If the :doc:`template file type <configuration>` is
    "script" it will also be made executable.

    If no filename is given for PATH, a default filename will be used. For more information
    about specifying the default filename, see :doc:`/default_filename`.

    EXAMPLES ::

      $ vscode-cli-helpers-open-file open a.py

    If ``a.py`` exists, opens it in VS Code and navigates to line 1. If ``a.py`` does not exist,
    determines the file type from the extension of ``a.py`` (``.py``). Then creates a
    file ``a.py`` and writes a template for the file type ``.py`` to the file. If the
    template type is "script", the file will also be made executable. Then opens the file
    in VS Code and navigates to line 1. ::

      $ vscode-cli-helpers-open-file open a

    If ``a`` exists, opens it in VS Code and navigates to line 1. If ``a`` does not exist,
    the file type will be determined from the default template (since ``--template`` option
    is not given). For example, if the default template is "Python", ``a.py`` will be
    created and made executable. Then the template will be written to the file
    before opening it in VSCode. ::

    \b
      $ vscode-cli-helpers-open-file open a:10
      $ vscode-cli-helpers-open-file a.py:10

    Sames as above but also navigates to line 10

    For more information about editing the template file, see :doc:`/template`.
    For information about specifying the file type of the templates, see :doc:`/configuration`.

    """
    OpenFile(path, template)


if __name__ == "__main__":  # pragma: no cover
    main()
