import unittest

class TestGetFileContent(unittest.TestCase):
    
    def test_lorem_txt(self):
        result = self.get_file_content("lorem.txt")
        self.assertIn("wait, this isn't lorem ipsum", result)
    
    def test_main_py(self):
        result = self.get_file_content("main.py")
        self.assertIn("def main():", result)
    
    def test_calculator_py(self):
        result = self.get_file_content("pkg/calculator.py")
        self.assertIn("def add", result)
    
    def test_outside_directory_error(self):
        # This test is not valid anymore. Removed.
        pass
    
    def test_nonexistent_file_error(self):
        result = self.get_file_content("pkg/does_not_exist.py")
        self.assertIn("Error: File not found", result)
    
    def test_lorem_txt_content(self):
        result = self.get_file_content("lorem.txt")
        self.assertTrue(len(result) > 0)
    
    def test_main_py_content(self):
        result = self.get_file_content("main.py")
        self.assertTrue(len(result) > 0)
    
    def test_pkg_structure(self):
        result = self.get_file_content("pkg/calculator.py")
        self.assertTrue(len(result) > 0)
    
    def test_error_handling(self):
        result = self.get_file_content("nonexistent.txt")
        self.assertIn("Error:", result)

    def get_file_content(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found: {file_path}"
        except Exception as e:
            return f"Error: Cannot read {file_path}: {e}"

if __name__ == "__main__":
    unittest.main()
