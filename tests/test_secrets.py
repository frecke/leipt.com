"""Exercise secret publication boundaries without accessing GitHub."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("site_secrets", "scripts/secrets.py")
secrets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(secrets)


class SecretSyncTests(unittest.TestCase):
    def setUp(self):
        self.args = patch("sys.argv", ["secrets.py", "sync"])
        self.env = patch.dict("os.environ", {"AGE_IDENTITY": "/external/test.agekey"})
        self.args.start()
        self.env.start()
        self.addCleanup(self.args.stop)
        self.addCleanup(self.env.stop)

    @patch.object(secrets.subprocess, "run")
    def test_failed_decryption_never_invokes_gh(self, run):
        run.side_effect = subprocess.CalledProcessError(1, ["age"])
        with self.assertRaises(subprocess.CalledProcessError):
            secrets.main()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0][0], "age")

    @patch.object(secrets.subprocess, "run")
    def test_empty_plaintext_never_invokes_gh(self, run):
        run.return_value = subprocess.CompletedProcess(["age"], 0, stdout=b"\n")
        with self.assertRaises(RuntimeError):
            secrets.main()
        self.assertEqual(run.call_count, 1)

    @patch.object(secrets.subprocess, "run")
    def test_publish_uses_stdin_and_explicit_repository_and_environment(self, run):
        plaintext = b"EXAMPLE=fake-test-value\n"
        run.return_value = subprocess.CompletedProcess(["age"], 0, stdout=plaintext)
        secrets.main()
        decrypt, publish = run.call_args_list
        self.assertEqual(
            decrypt.args[0],
            [
                "age",
                "--decrypt",
                "--identity",
                "/external/test.agekey",
                str(Path("secrets/onecom-preview.env.age")),
            ],
        )
        self.assertEqual(
            publish.args[0],
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
        )
        self.assertEqual(publish.kwargs["input"], plaintext)
        self.assertTrue(publish.kwargs["check"])

    @patch.object(secrets.subprocess, "run")
    def test_github_failure_propagates(self, run):
        run.side_effect = [
            subprocess.CompletedProcess(["age"], 0, stdout=b"EXAMPLE=fake\n"),
            subprocess.CalledProcessError(1, ["gh"]),
        ]
        with self.assertRaises(subprocess.CalledProcessError):
            secrets.main()


class AgeRoundTripTests(unittest.TestCase):
    def test_real_age_encrypt_decrypt(self):
        script = Path("scripts/secrets.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            identity = Path(directory) / "test.agekey"
            subprocess.run(
                ["age-keygen", "-o", str(identity)], capture_output=True, check=True
            )
            recipient = (
                subprocess.run(
                    ["age-keygen", "-y", str(identity)], capture_output=True, check=True
                )
                .stdout.decode()
                .strip()
            )
            payload = b"EXAMPLE=fake-roundtrip-value\n"
            subprocess.run(
                [sys.executable, str(script), "encrypt"],
                input=payload,
                cwd=directory,
                env={**os.environ, "AGE_RECIPIENT": recipient},
                capture_output=True,
                check=True,
            )
            encrypted = Path(directory) / secrets.ENCRYPTED
            self.assertNotIn(payload, encrypted.read_bytes())
            decrypted = subprocess.run(
                ["age", "--decrypt", "-i", str(identity), str(encrypted)],
                capture_output=True,
                check=True,
            ).stdout
            self.assertEqual(decrypted, payload)


if __name__ == "__main__":
    unittest.main()
