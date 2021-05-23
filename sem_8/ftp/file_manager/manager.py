from commands import *
from exceptions import *

cmd_dict = {
    "echo": echo,
    "pwd": pwd,
    "ls": dir_list,
    "mkdir": make_dir,
    "rm": remove,
    "rmdir": remove_dir,
    "cd": change_dir,
    "touch": touch,
    "write": write,
    "cat": read,
    "cp": copy,
    "mv": move,
    "rename": rename,
}


def split(row: str):
    """
    Separates command line into command name, arguments and flags
    :param row: command line
    :return: dict with keys: cmd, args, flags
    """
    res_args = []
    res_cmd, *args = row.split(" ", 1)
    res_flags = set()
    if len(args) > 0:
        args = args[0]
        if args.count("\"") % 2 != 0:
            raise IncorrectInputException
        quoted = False
        for item in args.split("\""):
            if quoted:
                res_args.append(item)
            else:
                for arg in item.split():
                    if arg[0] == "-":
                        res_flags.add(arg)
                    else:
                        res_args.append(arg)
            quoted = not quoted
    return {
        "cmd": res_cmd,
        "args": res_args,
        "flags": res_flags
    }


def execute(row: str):
    """
    Executes command from row
    :param row: inputted line
    """
    try:
        parsed = split(row)
        output = cmd_dict[parsed["cmd"]](*parsed["args"], flags=parsed["flags"])
        if output is not None: return output
    except KeyError:
        return "Invalid command"
    except TypeError:
        return "Invalid arguments"
    except IncorrectInputException:
        return "Incorrect input"

