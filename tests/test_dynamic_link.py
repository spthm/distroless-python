import unittest
from ctypes import CDLL, create_string_buffer
from ctypes.util import find_library


class TestSharedLibraries(unittest.TestCase):
    def test_find_libc(self):
        libc = CDLL(find_library("c"))
        self.assertIsNotNone(libc)

    def test_find_extras(self):
        for l in ["gcc_s", "gomp", "stdc++"]:
            lib = find_library(l)
            self.assertIsNotNone(lib)

    def test_use_libc_sprintf(self):
        libc = CDLL(find_library("c"))
        s = create_string_buffer(50)
        libc.sprintf(s, b"Hello, %s\n", b"World!")
        self.assertEqual(s.value, b"Hello, World!\n")


if __name__ == "__main__":
    unittest.main()
