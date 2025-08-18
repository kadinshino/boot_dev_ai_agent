from functions.get_file_content import get_file_content
import unittest
import os

class TestGetFileContent(unittest.TestCase):
    
    def test_lorem_txt(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertIn("wait, this isn't lorem ipsum", result)
    
    def test_main_py(self):
        result = get_file_content("calculator", "main.py")
        self.assertIn("def main():", result)
    
    def test_calculator_py(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertIn("def add", result)
    
    def test_outside_directory_error(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertIn("Error: Cannot read", result)
    
    def test_nonexistent_file_error(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertIn("Error: File not found", result)
    
    def test_lorem_txt_content(self):
        result = get_file_content("calculator", "lorem.txt")
        self.assertTrue(len(result) > 0)
    
    def test_main_py_content(self):
        result = get_file_content("calculator", "main.py")
        self.assertTrue(len(result) > 0)
    
    def test_pkg_structure(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertTrue(len(result) > 0)
    
    def test_error_handling(self):
        result = get_file_content("calculator", "nonexistent.txt")
        self.assertIn("Error:", result)

if __name__ == "__main__":
    unittest.main()
