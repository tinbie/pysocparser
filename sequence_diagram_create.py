import sys
from art import *
from tabulate import tabulate


# constants
SCOPE_LOCAL = "static"
TYPE_RETURN = ["void", "GOAL_STATUS_T"]


# return a list of static functions
def static_functions_get(file):
    static_functions = []
    file.seek(0)
    for line in file:
        if any(element in line for element in TYPE_RETURN):
            if SCOPE_LOCAL in line:
                static_functions.append(line.replace("\n", ""))
    return static_functions


# return a list of public functions
def public_functions_get(file):
    public_functions = []
    file.seek(0)
    for line in file:
        if any(element in line for element in TYPE_RETURN):
            if not SCOPE_LOCAL in line:
                if "(" in line:
                    public_functions.append(line.replace("\n", ""))
    return public_functions


# get row number of function in file
def function_row_get(file, function):
    file.seek(0)
    for linenumber, line in enumerate(file):
        if function + "(" in line:
            return linenumber
    # did not found function
    return 0


# main
def main():
    # fetch parameters
    module_name = sys.argv[1]
    function_start = sys.argv[2]

    # open file and search for start
    module_file = open(module_name, "r")
    function_start_line = function_row_get(module_file, function_start)

    # catch emptyness
    if 0 == function_start_line:
        print("passed function is unknown")
        exit()

    # get static functions
    static_functions = static_functions_get(module_file)
    print("\nSTATIC FUNCTIONS")
    print(tabulate(list(map(lambda x:[x], static_functions))))

    # get public functions
    public_functions = public_functions_get(module_file)
    print("\nPUBLIC FUNCTIONS")
    print(tabulate(list(map(lambda x:[x], public_functions))))

    # skip lines and start processing
    module_file.seek(0)
    for lines_skip in range(function_start_line):
        next(module_file)
    for line in module_file:
        # searching for function call in line
        if "(" in line:
        # if public -> print and return
        # if static -> search for static function and recursive
        print(line)
        break

    # close file
    module_file.close()


if __name__ == "__main__":
    main()

