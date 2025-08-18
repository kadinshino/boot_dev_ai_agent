from functions.run_python import run_python_file

def run_tests():
    test_cases = [
        ("calculator", "main.py"),                          # no args
        ("calculator", "main.py", ["3 + 5"]),               # with argument
        ("calculator", "tests.py"),                         # run itself
        ("calculator", "../main.py"),                       # should trigger security error
        ("calculator", "nonexistent.py")                    # should trigger file-not-found
    ]

    for i, test in enumerate(test_cases, 1):
        if len(test) == 2:
            working_directory, file_path = test
            args = []
        else:
            working_directory, file_path, args = test

        result = run_python_file(working_directory, file_path, args)
        print(f"\nTest Case {i}:\n{result}")

if __name__ == "__main__":
    run_tests()
