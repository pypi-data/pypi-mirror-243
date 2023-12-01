import logging
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from vscode_cli_helpers.open_file.config import Config
from vscode_cli_helpers.open_file.exceptions import OpenFileException


class OpenFile:
    def __init__(self, path: Optional[str], template_name: Optional[str]) -> None:
        self.config = Config()
        if template_name is None:
            template_name = self.config.get_default_template_name()
        if path is None:
            path = self.config.get_default_filename(template_name)
        self.path = path
        self.template_name = template_name
        filename = Path(path).name
        dir_ = Path(path).parent
        (basename, line_no) = (
            filename.split(":") if ":" in filename else (filename, None)
        )
        if basename is not None:
            filename = self.add_extension(basename)
        workspace = self.find_code_workspace(dir_)
        path2 = Path(dir_) / filename
        if not path2.exists():
            self.prepare_new_file(path2)
        else:
            logging.info(f"File exists: {path}")
        if line_no is not None:
            filename = f"{filename}:{line_no}"
        cmd = ["code"]
        if platform.system() == "Windows":  # pragma: no cover
            # See: https://stackoverflow.com/a/32799942/2173773
            tmp = shutil.which("code.cmd")
            if tmp is None:
                raise OpenFileException("Could not find code.cmd")
            cmd = [tmp]
        elif platform.system() == "Darwin":
            # cmd = (
            #    "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
            # )
            cmd = ["open", "-a", "Visual Studio Code"]
        cmd.extend(["-g", filename, workspace])
        logging.info(f"Running: {cmd} in directory: {dir_}, workspace: {workspace}")
        subprocess.Popen(cmd, cwd=dir_, start_new_session=True)

    def add_extension(self, name: str) -> str:
        """Add the file extension if it is missing.

        Examples:

        * ``hello" -> ``hello.cpp``
        * ``hello.cpp" -> ``hello.cpp``
        * ``.cpp`` -> ``.cpp.cpp``
        * ``.hello`` -> ``.hello.cpp`` (note: not ``.hello``)
        * ``a.hello`` -> ``a.hello.cpp`` (note: not ``a.hello``)
        * ``hello.`` -> ``hello.cpp`` (note: not ``hello..cpp``)
        """
        parts = name.rsplit(sep=".", maxsplit=1)
        ext = self.config.get_template_extension(self.template_name)
        ext = ext.lstrip(".")
        if len(parts) == 1:
            return parts[0] + f".{ext}"
        else:  # len(parts) == 2:
            body = parts[0]
            ext2 = parts[1]
            if len(body) == 0:
                return f".{ext2}.{ext}"
            elif len(ext2) == 0:
                return body + f".{ext}"
            elif ext2 == ext:
                return parts[0] + f".{ext}"
            else:
                return body + f".{ext2}.{ext}"

    def find_code_workspace(self, dir_: Path) -> str:
        """Find the VSCode workspace for the given path."""
        workspaces = list(dir_.glob("*.code-workspace"))
        if len(workspaces) == 1:
            return Path(workspaces[0]).name
        else:
            return "."

    def prepare_new_file(self, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.config.get_template(self.template_name))
        logging.info(f"Creating file: {path}")
        if platform.system() == "Windows":
            logging.info("Not making file executable on Windows")
        else:
            if self.config.is_script(self.template_name):
                os.chmod(path, 0o755)
                logging.info(f"Setting file permissions to 755: {path}")
            else:
                logging.info(
                    f"Not script file type {self.template_name}. "
                    f"Not setting file permissions: {path}"
                )
