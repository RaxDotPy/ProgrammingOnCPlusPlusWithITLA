import os
import unittest

from app.main import collect_cpp_source_files


class SourceFilesTests(unittest.TestCase):
    def test_collect_cpp_source_files_returns_project_cpp_files(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        src_dir = os.path.join(project_root, "src")

        files = collect_cpp_source_files(src_dir)

        self.assertTrue(files)
        self.assertTrue(all(isinstance(item, dict) and "path" in item and item["path"].endswith(".cpp") for item in files))
        self.assertTrue(any("main.cpp" in item["path"].lower() for item in files) or any("ejercicio" in item["path"].lower() for item in files))


if __name__ == "__main__":
    unittest.main()
