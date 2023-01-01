import pkgutil
import unittest
import warnings

exclude = frozenset(
    (
        # Windows only.
        "asyncio.windows_events",
        "asyncio.windows_utils",
        "ctypes.wintypes",
        "encodings.cp65001",
        # Import Windows-only modules.
        "encodings.oem",  # imports 'oem_encode' from 'codecs'
        "encodings.mbcs",  # imports 'mbcs_encode' from 'codecs'
        "distutils._msvccompiler",  # imports 'winreg'
        "distutils.command.bdist_msi",  # imports 'msilib'
        "distutils.msvc9compiler",  # imports 'winreg'
        "multiprocessing.popen_spawn_win32",  # imports 'msvcrt'
        # Not available in -slim Python images.
        "dbm.ndbm",
        # Can't be imported stand-alone; fails due to local import of pgen2.
        "lib2to3.pgen2.conv",
        # Expect command line args.
        "lib2to3.__main__",
        "venv.__main__",
        # Prints unwanted stdout.
        "unittest.__main__",
    )
)


def _onerror(name):
    # walk_packages will swallow ImportErrors if we do not provide an onerror
    # function; make sure this script fails in that case.
    raise RuntimeError(f"failed to import package: {name}")


class TestSmokeTestStdlib(unittest.TestCase):
    def test_import_all(self):
        # Deprecation warnings for to-be-removed stdlib packages are common but not
        # useful to see here.
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        for info in pkgutil.walk_packages(onerror=_onerror):
            name = info.name

            if name in exclude:
                print("skipping explicitly excluded module {}".format(name))
                continue

            print("importing {}".format(name))
            __import__(name)


if __name__ == "__main__":
    unittest.main()
