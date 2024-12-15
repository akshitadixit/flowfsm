import unittest
import json
import os
from flowfsm.config.parser import load_json_config


class TestLoadJSONConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = "test_json_files"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory and its contents after each test
        for file_name in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, file_name)
            os.remove(file_path)
        os.rmdir(self.test_dir)

    def create_test_file(self, file_name, content):
        file_path = os.path.join(self.test_dir, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        return file_path

    def test_load_json_config_valid(self):
        content = json.dumps({"key": "value"})
        file_path = self.create_test_file("valid.json", content)
        result = load_json_config(file_path)
        self.assertEqual(result, {"key": "value"})

    def test_load_json_config_empty(self):
        content = json.dumps({})
        file_path = self.create_test_file("empty.json", content)
        result = load_json_config(file_path)
        self.assertEqual(result, {})

    def test_load_json_config_invalid(self):
        content = "{key: value}"  # Invalid JSON format
        file_path = self.create_test_file("invalid.json", content)
        with self.assertRaises(json.JSONDecodeError):
            load_json_config(file_path)

    def test_load_json_config_nonexistent_file(self):
        file_path = os.path.join(self.test_dir, "nonexistent.json")
        with self.assertRaises(FileNotFoundError):
            load_json_config(file_path)

if __name__ == '__main__':
    unittest.main()