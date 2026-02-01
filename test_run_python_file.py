from functions.run_python_file import run_python_file


def main():
    # Test 1: Run main.py without arguments (should show usage)
    print("Test 1: Run calculator/main.py (no arguments):")
    print(run_python_file("calculator", "main.py"))
    print()

    # Test 2: Run main.py with calculation argument
    print("Test 2: Run calculator/main.py with '3 + 5':")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    # Test 3: Run tests.py (should run tests successfully)
    print("Test 3: Run calculator/tests.py:")
    print(run_python_file("calculator", "tests.py"))
    print()

    # Test 4: Try to run file outside working directory (should error)
    print("Test 4: Try to run ../main.py (should error):")
    print(run_python_file("calculator", "../main.py"))
    print()

    # Test 5: Try to run non-existent file (should error)
    print("Test 5: Try to run nonexistent.py (should error):")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    # Test 6: Try to run a non-Python file (should error)
    print("Test 6: Try to run lorem.txt (should error):")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
