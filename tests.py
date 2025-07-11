# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# Lesson 2 tests
# get_files_info("calculator", ".")
# get_files_info("calculator", "pkg")
# get_files_info("calculator", "/bin")
# get_files_info("calculator", "../")

# Lesson 3 tests
# get_file_content("calculator", "lorem.txt")
# get_file_content("calculator", "main.py")
# get_file_content("calculator", "pkg/calculator.py")
# get_file_content("calculator", "/bin/cat")

# Lesson 4 tests
# write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

# Lesson 5 tests
# run_python_file("calculator", "main.py")
# run_python_file("calculator", "tests.py")
# run_python_file("calculator", "../main.py")
# run_python_file("calculator", "nonexistent.py")

def test():
    result = run_python_file("calculator", "main.py")
    print(result)

    result = run_python_file("calculator", "tests.py")
    print(result)

    result = run_python_file("calculator", "../main.py")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test()
