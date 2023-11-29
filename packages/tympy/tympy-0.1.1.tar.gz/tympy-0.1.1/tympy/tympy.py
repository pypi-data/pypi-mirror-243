import time
import importlib


def compare(*args):
    """
    This function displays the output and execution times of two or more Python scripts.
    """

    if len(args) != 3:
        raise ValueError(
            "The compare function accepts exactly 3 arguments.")

    if isinstance(args[0], list):
        files = args[0]
    else:
        files = [args[0]] * len(args[1])

    if isinstance(args[1], list):
        functions = args[1]
    else:
        functions = [args[1]] * len(files)

    if isinstance(args[2], list):
        arguments = args[2]
    else:
        arguments = [args[2]] * len(functions)

    # Check if the length of functions and arguments is either 1 or equal to the length of files
    if len(functions) != 1 and len(functions) != len(files):
        raise ValueError(
            "The length of functions must be either 1 or equal to the length of files.")
    if len(arguments) != 1 and len(arguments) != len(files):
        raise ValueError(
            "The length of arguments must be either 1 or equal to the length of files.")

    execution_times = []

    # for i in range(len(files)):
    #     script_path = files[i]
    #     function_name = functions[i]
    #     arg = arguments[i]
    for i, script_path in enumerate(files):
        function_name = functions[i]
        arg = arguments[i]

        module_name = script_path.split('/')[-1].split('.')[0]
        module = importlib.import_module(module_name)

        function = getattr(module, function_name)

        start_time = time.time()
        # Unpack the argument if it's a tuple
        if isinstance(arg, tuple):
            stdout = function(*arg)
        else:
            stdout = function(arg)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
        print(f"\n◢ {script_path}:")
        print(f"- Output: {stdout}")

        print(
            f"\n======= Execution time for {script_path}: {execution_time} seconds")

    print("\n====================================")
    min_time = min(execution_times)
    max_time = max(execution_times)
    min_scripts = [files[i]
                   for i, time in enumerate(execution_times) if time == min_time]
    max_scripts = [files[i]
                   for i, time in enumerate(execution_times) if time == max_time]
    if len(min_scripts) > 1:
        print(f"⇲ {', '.join(min_scripts)} are the fastest")
    else:
        print(f"⇲ {', '.join(min_scripts)} is the fastest")
    if len(max_scripts) > 1:
        print(f"⇲ {', '.join(max_scripts)} are the slowest")
    else:
        print(f"⇲ {', '.join(max_scripts)} is the slowest")
    print("====================================\n")
