import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from flutes.log import log
from flutes.run import CommandResult, error_wrapper, run_command

__all__ = [
    "run_docker_command",
    "verify_docker_image",
]


def run_docker_command(command: Union[str, List[str]], cwd: Optional[str] = None,
                       user: Optional[Union[int, Tuple[int, int]]] = None,
                       directory_mapping: Optional[Dict[str, str]] = None,
                       timeout: Optional[float] = None, **kwargs) -> CommandResult:
    r"""Run a command inside a container based on the ``gcc-custom`` Docker image.

    :param command: The command to run. Should be either a `str` or a list of `str`. Note: they're treated the same way,
        because a shell is always spawn in the entry point.
    :param cwd: The working directory of the command to run. If None, uses the default (probably user home).
    :param user: The user ID to use inside the Docker container. Additionally, group ID can be specified by passing
        a tuple of two `int`\ s for this argument. If not specified, the current user and group IDs are used. As a
        special case, pass in ``0`` to run as root.
    :param directory_mapping: Mapping of host directories to container paths. Mapping is performed via "bind mount".
    :param timeout: Maximum running time for the command. If running time exceeds the specified limit,
        ``subprocess.TimeoutExpired`` is thrown.
    :param kwargs: Additional keyword arguments to pass to :meth:`ghcc.utils.run_command`.
    """
    # Validate `command` argument, and append call to `bash` if `shell` is True.
    if isinstance(command, list):
        command = ' '.join(command)
    command = f"'{command}'"

    # Construct the `docker run` command.
    docker_command = ["docker", "run", "--rm"]
    for host, container in (directory_mapping or {}).items():
        docker_command.extend(["-v", f"{os.path.abspath(host)}:{container}"])
    if cwd is not None:
        docker_command.extend(["-w", cwd])

    # Assign user and group IDs based on `user` argument.
    if user != 0:
        user_id: Union[str, int] = "`id -u $USER`"
        group_id: Union[str, int] = "`id -g $USER`"
        if user is not None:
            if isinstance(user, tuple):
                user_id, group_id = user
            else:
                user_id = user
        docker_command.extend(["-e", f"LOCAL_USER_ID={user_id}"])
        docker_command.extend(["-e", f"LOCAL_GROUP_ID={group_id}"])

    docker_command.append("gcc-custom")
    if timeout is not None:
        # Timeout is implemented by calling `timeout` inside Docker container.
        docker_command.extend(["timeout", f"{timeout}s"])
    docker_command.append(command)
    ret = run_command(' '.join(docker_command), shell=True, **kwargs) # original line
        
    # Check whether exceeded timeout limit by inspecting return code.
    if ret.return_code == 124:
        assert timeout is not None
        raise error_wrapper(subprocess.TimeoutExpired(ret.command, timeout, output=ret.captured_output))
    return ret

def run_docker_command_other(command: Union[str, List[str]], cwd: Optional[str] = None,
                       user: Optional[Union[int, Tuple[int, int]]] = None,
                       directory_mapping: Optional[Dict[str, str]] = None,
                       timeout: Optional[float] = None, **kwargs) -> CommandResult:
    r"""Run a command inside a container based on the ``gcc-custom`` Docker image.

    :param command: The command to run. Should be either a `str` or a list of `str`. Note: they're treated the same way,
        because a shell is always spawn in the entry point.
    :param cwd: The working directory of the command to run. If None, uses the default (probably user home).
    :param user: The user ID to use inside the Docker container. Additionally, group ID can be specified by passing
        a tuple of two `int`\ s for this argument. If not specified, the current user and group IDs are used. As a
        special case, pass in ``0`` to run as root.
    :param directory_mapping: Mapping of host directories to container paths. Mapping is performed via "bind mount".
    :param timeout: Maximum running time for the command. If running time exceeds the specified limit,
        ``subprocess.TimeoutExpired`` is thrown.
    :param kwargs: Additional keyword arguments to pass to :meth:`ghcc.utils.run_command`.
    """
    # Validate `command` argument, and append call to `bash` if `shell` is True.
    if isinstance(command, list):
        command = ' '.join(command)
    command = f"'{command}'"

    # Construct the `docker run` command.
    docker_command = ["docker", "run", "--rm"]
    for host, container in (directory_mapping or {}).items():
        docker_command.extend(["-v", f"{os.path.abspath(host)}:{container}"])
    if cwd is not None:
        docker_command.extend(["-w", cwd])

    # Assign user and group IDs based on `user` argument.
    if user != 0:
        user_id: Union[str, int] = "`id -u $USER`"
        group_id: Union[str, int] = "`id -g $USER`"
        if user is not None:
            if isinstance(user, tuple):
                user_id, group_id = user
            else:
                user_id = user
        docker_command.extend(["-e", f"LOCAL_USER_ID={user_id}"])
        docker_command.extend(["-e", f"LOCAL_GROUP_ID={group_id}"])
        docker_command.extend(["-e", "PYTHONUNBUFFERED=1"]) # added

    docker_command.append("gcc-custom")
    if timeout is not None:
        # Timeout is implemented by calling `timeout` inside Docker container.
        docker_command.extend(["timeout", f"{timeout}s"])
    docker_command.append(command)

    del kwargs["return_output"] # needed since we use our own subprocess.run command
    ret = run_command(' '.join(docker_command), shell=True, verbose=True, return_output=True, **kwargs) # original line
    
    cwd_str = str(cwd) if cwd is not None else None
    ret = subprocess.run(' '.join(docker_command), check=True, capture_output=True, shell=True,
            timeout=timeout, cwd=cwd_str, **kwargs)
    #print(f"RET {ret.stdout.decode('utf8')}")
    #print(f"RET ERROR {ret.stderr}")
    ret = CommandResult(' '.join(docker_command), ret.returncode, None)
        
    # Check whether exceeded timeout limit by inspecting return code.
    if ret.return_code == 124:
        assert timeout is not None
        raise error_wrapper(subprocess.TimeoutExpired(ret.command, timeout, output=ret.captured_output))
    return ret


def verify_docker_image(verbose: bool = False, print_checked_paths: bool = False) -> bool:
    r"""Checks whether the Docker image is up-to-date. This is done by verifying the modification dates for all library
    files are earlier than the Docker image build date.

    :param verbose: If ``True``, prints out error message telling the user to rebuild Docker image.
    :param print_checked_paths: If ``True``, prints out paths of all checked files.
    """
    output = run_command(
        ["docker", "image", "ls", "gcc-custom", "--format", "{{.CreatedAt}}"], return_output=True).captured_output
    assert output is not None
    image_creation_time_string = output.decode("utf-8").strip()
    image_creation_timestamp = datetime.strptime(image_creation_time_string, "%Y-%m-%d %H:%M:%S %z %Z").timestamp()

    repo_root: Path = Path(__file__).parent.parent.parent
    paths_to_check = ["ghcc", "scripts", ".dockerignore", "Dockerfile", "requirements.txt"]
    paths_to_ignore = ["ghcc/parse", "ghcc/database.py", "scripts/fake_libc_include"]
    prefixes_to_ignore = [str(repo_root / path) for path in paths_to_ignore]
    max_timestamp = 0.0
    for repo_path in paths_to_check:
        path = str(repo_root / repo_path)
        if os.path.isfile(path) and not any(path.startswith(prefix) for prefix in prefixes_to_ignore):
            if print_checked_paths:
                print(path)
            max_timestamp = max(max_timestamp, os.path.getmtime(path))
        else:
            for subdir, dirs, files in os.walk(path):
                if subdir.endswith("__pycache__"):
                    continue
                for f in files:
                    file_path = os.path.join(subdir, f)
                    if not any(file_path.startswith(prefix) for prefix in prefixes_to_ignore):
                        if print_checked_paths:
                            print(file_path)
                        max_timestamp = max(max_timestamp, os.path.getmtime(file_path))
    up_to_date = max_timestamp <= image_creation_timestamp

    if not up_to_date and verbose:
        image_path = os.path.relpath(os.path.join(__file__, "..", "..", ".."), os.getcwd())
        log("ERROR: Your Docker image is out-of-date. Please rebuild the image by: "
            f"`docker build -t gcc-custom {image_path}`", "error", force_console=True)
    return up_to_date
