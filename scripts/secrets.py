"""Keep local secrets age-encrypted; publish via gh without plaintext files."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ENCRYPTED = Path("secrets/onecom-preview.env.age")


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Set {name} before running this command")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("encrypt", "sync"))
    args = parser.parse_args()
    if args.operation == "encrypt":
        recipient = required("AGE_RECIPIENT")
        if sys.stdin.isatty():
            raise RuntimeError("Pass dotenv secrets on stdin")
        encrypted = subprocess.run(
            ["age", "--encrypt", "--recipient", recipient],
            stdin=sys.stdin.buffer,
            capture_output=True,
            check=True,
        ).stdout
        ENCRYPTED.parent.mkdir(exist_ok=True)
        ENCRYPTED.write_bytes(encrypted)
    else:
        # Complete decryption before invoking gh: a wrong key cannot publish
        # partial data. Plaintext stays in memory and the child's stdin.
        plaintext = subprocess.run(
            [
                "age",
                "--decrypt",
                "--identity",
                required("AGE_IDENTITY"),
                str(ENCRYPTED),
            ],
            capture_output=True,
            check=True,
        ).stdout
        if not plaintext.strip():
            raise RuntimeError("Decrypted secrets are empty; refusing to publish")
        subprocess.run(
            [
                "gh",
                "secret",
                "set",
                "--repo",
                "frecke/leipt.com",
                "--env",
                "onecom-preview",
                "--env-file",
                "-",
            ],
            input=plaintext,
            check=True,
        )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        # Do not print subprocess output; it may contain secret material.
        sys.exit(
            f"Secret operation failed ({type(error).__name__}). Check keys/config."
        )
