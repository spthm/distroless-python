import subprocess
import sys
import unittest


class TestShell(unittest.TestCase):
    def test_run_python(self):
        r = subprocess.run(
            f"{sys.executable} --version", capture_output=True, check=True, shell=True
        )

        major, minor, micro, *_ = sys.version_info
        self.assertEqual(r.stdout.decode("utf-8"), f"Python {major}.{minor}.{micro}\n")


if __name__ == "__main__":
    unittest.main()
