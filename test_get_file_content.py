from functions.get_file_content import get_file_content
from config import MAX_CHARS


def main():
    # Test 1: Lorem ipsum file truncation test
    print("Test 1: Lorem ipsum file (should be truncated):")
    result = get_file_content("calculator", "lorem.txt")
    print(f"Content length: {len(result)} characters")
    if len(result) > MAX_CHARS:
        print("Last 100 characters:")
        print(result[-100:])
    print()

    # Test 2: Read main.py
    print("Test 2: calculator/main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    # Test 3: Read pkg/calculator.py
    print("Test 3: calculator/pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # Test 4: Try to read /bin/cat (should error - outside working directory)
    print("Test 4: /bin/cat (should error):")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # Test 5: Try to read non-existent file (should error)
    print("Test 5: calculator/pkg/does_not_exist.py (should error):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
