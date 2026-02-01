from functions.write_file import write_file


def main():
    # Test 1: Overwrite existing lorem.txt file
    print("Test 1: Write to calculator/lorem.txt:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    # Test 2: Create a new file in pkg subdirectory
    print("Test 2: Write to calculator/pkg/morelorem.txt:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    # Test 3: Try to write outside working directory (should error)
    print("Test 3: Try to write to /tmp/temp.txt (should error):")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()
