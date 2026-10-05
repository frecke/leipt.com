"""Upload generated files to a marked one.com preview directory, without deletes."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import tempfile
from errno import ENOENT

import paramiko


TARGET = "leipt-preview"
MARKER = ".leipt-deploy-root"
MARKER_VALUE = b"leipt-preview-v1\n"


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required secret: {name}")
    return value


def main() -> None:
    public = Path("public")
    if not (public / "index.html").is_file():
        raise RuntimeError("Missing Hugo output: public/index.html")

    host = required("ONECOM_SFTP_HOST")
    user = required("ONECOM_SFTP_USER")
    password = required("ONECOM_SFTP_PASSWORD")
    known_hosts = required("ONECOM_SFTP_KNOWN_HOSTS")
    port = int(required("ONECOM_SFTP_PORT"))
    if not (1 <= port <= 65535):
        raise RuntimeError("Invalid SFTP port")

    with tempfile.TemporaryDirectory() as temporary:
        known_hosts_file = Path(temporary) / "known_hosts"
        known_hosts_file.write_text(known_hosts + "\n", encoding="utf-8")
        client = paramiko.SSHClient()
        client.load_host_keys(str(known_hosts_file))
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(hostname=host, port=port, username=user, password=password,
                       look_for_keys=False, allow_agent=False, timeout=20)
        try:
            sftp = client.open_sftp()
            try:
                target_stat = sftp.lstat(TARGET)
                if not stat.S_ISDIR(target_stat.st_mode):
                    raise RuntimeError("Preview target is not a directory")
                with sftp.open(f"{TARGET}/{MARKER}", "rb") as marker:
                    if marker.read() != MARKER_VALUE:
                        raise RuntimeError("Preview marker mismatch; refusing upload")
                for local in sorted(public.rglob("*")):
                    relative = local.relative_to(public).as_posix()
                    if relative == MARKER or local.is_symlink():
                        raise RuntimeError("Invalid generated path")
                    remote = f"{TARGET}/{relative}"
                    if local.is_dir():
                        try:
                            remote_stat = sftp.lstat(remote)
                        except IOError as error:
                            if error.errno != ENOENT:
                                raise
                            sftp.mkdir(remote)
                            remote_stat = sftp.lstat(remote)
                        if not stat.S_ISDIR(remote_stat.st_mode):
                            raise RuntimeError(f"Remote path is not a directory: {relative}")
                    elif local.is_file():
                        try:
                            remote_stat = sftp.lstat(remote)
                        except IOError as error:
                            if error.errno != ENOENT:
                                raise
                        else:
                            if not stat.S_ISREG(remote_stat.st_mode):
                                raise RuntimeError(f"Remote path is not a regular file: {relative}")
                        sftp.put(str(local), remote)
            finally:
                sftp.close()
        finally:
            client.close()


if __name__ == "__main__":
    main()
