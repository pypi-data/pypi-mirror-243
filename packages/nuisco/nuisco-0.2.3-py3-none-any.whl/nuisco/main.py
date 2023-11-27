from . import build
from . import template
import sys
from typing import Union, List, Dict
import re

def error(i, command_string):
    print(command_string)
    print(" "*i+"^")

def seperate_pre_args(command_line, arg_struct: Union[List[str], Dict[str, Union[Dict, List[str]]]]):
    """arg_struct example : {
        "cmd1": ["cmd12", "cmd13"],
        "cmd2": {"cmd22": ["cmd221"], "cmd23": {...}}
    }
    -> structure
    cmd1
        cmd12
        cmd13
    cmd2
        cmd22
            cmd221
        cmd23
            ..."""
    split = command_line.split(" -") # Using one dash to avoid wrong argument declarations
    pre_args, others = split[0], "-" + " -".join(split[1:]) if len(split[1:]) > 0 else "" + " -".join(split[1:]) # Join only fills the inner spaces with the string "glue"
    struct_lst = []
    current_struct = arg_struct # using that by default dict iter is key, so we can iter list and key and throw error if value error
    #print(command_line)
    try:
        pre_args_lst = pre_args.split(" ")
        for i, call in enumerate(pre_args_lst):
            if call in current_struct or current_struct[0] == "ANY": # could check for instance, but just is works fine as the default for "in dict" is "in dict.keys()"
                struct_lst.append(call)
                if not i == len(pre_args_lst)-1:
                    current_struct = current_struct[call] # Will throw an error, if the call stack is longer than arg_struct
            else:
                raise IndexError
    except TypeError:
        print("Too many call layers for arg_struct")
        sys.exit(1)
    except (IndexError, KeyError):
        print(i, call, current_struct)
        print("Wrong call in current_struct")
        sys.exit(1)
    #else: print(f"Call stack is {' '.join(struct_lst)}") # Debug
    return (struct_lst, others)

def parse_args(command_string, all_args: set, needed_args: set):
    #args = re.findall(r'--(.*?)(?=\s*--|\s*$)', command_string)
    #pattern = r'(?:^|\s+)(--[a-zA-Z]+=[^,]+(?:, [^,]+)?)(?=\s+|$)'
    all_args = all_args or {} # Dict
    needed_args = list(set(needed_args)) or list(set()) # Subset of all_args or set of all_args
    arg_switch, args = 0, {}
    last_char, arg = None, ""
    value, args_lst = "", []
    for i, char in enumerate(command_string):
        #print(i==len(command_string)-1, char)
        if arg_switch and not arg_switch == 2: # At arg namespace
            if not char == "-" and not char == " ":
                if char == "=" and not (i >= len(command_string)-1 or command_string[i+1] == " "):
                    arg_switch = 2
                    args[arg] = []
                    args_lst.append(arg)
                elif char == "=" and (i >= len(command_string)-1 or command_string[i+1] == " "):
                    print("Empty arguments aren't allowed")
                    error(i, command_string)
                    sys.exit(1)
                elif (char.isalpha() or char == "_" and len(arg) == 0) or ((char.isalnum() or char == "_") and not len(arg) == 0):
                    arg += char
                elif (char.isnumeric() or not (char.isalpha() or char == "_") and len(arg) == 0):
                    print("Only Letters and underscores are allowed at the start of arg namespace")
                    error(i, command_string)
                    sys.exit(1)
                elif not (char.isalpha() or char == "_") and not len(arg) == 0:# r"\w"
                    print("Only numbers, letters and underscores are allowed in arg namespace")
                    error(i, command_string)
                    sys.exit(1)
                else:
                    print("Empty arguments aren't allowed")
                    error(i, command_string)
                    sys.exit(1)
            else:
                print("Dashes or spaces aren't allowed in arg namespace")
                error(i, command_string)
                sys.exit(1)
        elif (char == "-" and last_char == "-"): # New arg declaration?
            if (i >= len(command_string)-1 or command_string[i+1] == " "):
                print("spaces after an arg declaration aren't allowed")
                error(i+1, command_string)
                sys.exit(1)
            elif (i >= 2 and command_string[i-2] != " "):
                print("Please seperate each arg declaration with a space")
                error(i-1, command_string)
                sys.exit(1)
            arg_switch = 1
            arg = ""
            value = ""
        elif (char == "-" and last_char == " " and (i >= len(command_string)-1 or not (command_string[i+1] == "-" or re.match(r".*?(?= |=)", command_string[i+1:]).group().isnumeric()))):
            print("Please declare arguments with two dashes")
            error(i, command_string)
            sys.exit(1)
        elif arg_switch == 2: # At arg value
            if char == " " and last_char == " ":
                print("Value error: No trailing spaces are allowed in arg values!")
                error(i, command_string)
                sys.exit(1)
            elif char == "=":
                print("Value error: No = allowed in value")
                error(i, command_string)
                sys.exit(1)
            elif char == "," and last_char == ",":
                print("Value error: No trailing commas are allowed in arg values!")
                error(i, command_string)
                sys.exit(1)
            elif char == " " and last_char != " ":
                args[arg] = args[arg] + value.split(",")
                value = ""
            elif i == len(command_string) - 1:
                value += char
                args[arg] = args[arg] + value.split(",")
                value = ""
            else:
                value += char
        last_char = char
        if len(set(args_lst)) != len(args_lst):
            print("Please only pass each argument once")
            print(f"{args_lst[-1]} was passed twice")
            sys.exit(1)
        if len(args_lst) > 0 and not args_lst[-1] in all_args:
            print("Please only pass accepted arguments")
            print(f"{args_lst[-1]} isn't accepted")
            print("Try one of these instead", all_args.keys())
            sys.exit(1)
    if not all(x in args_lst for x in needed_args):
        print(f"Not all needed_args ({needed_args}) passed")
        sys.exit(1)
    # Remove empty args
    args = {key: [arg for arg in args if arg] for key, args in args.items()}
    # Convert lists with a single item to that item
    for arg in args: # iterating with zip trough args.items() unneeded
        if isinstance(args[arg], list) and len(args[arg]) == 1 and not all_args[arg] == list:
            args[arg] = args[arg][0]
    for arg in args: # Turn them into their classes
        try:
            args[arg] = all_args[arg](args[arg])
        except Exception as e:
            print(f"You passed the wrong type for arg {arg}\nIt should be {all_args[arg]}")
            sys.exit(1)
    return args

def console_script(command_list=sys.argv):
    # Format : nuisca subcmd --args --arglst
    # Example : nuisca build --arg=arg --arglst=123, 1222 --arglst=123 1222 --arglst=123,1222 --arglst=123, 1222 123 1222, 123,1222
    # Output --> nuisca.build(arg=arg, arglst=123, 1222, 123, 1222, 123, 1222, 123, 1222, 123, 1222, 123, 1222)
    command_list[0] = command_list[0].split("\\")[-1] # First arg is location of package-dir
    if len(command_list) < 2:
        print("Usage: nuisco <subcommand> [--args]")
        sys.exit(1)
    elif command_list[1].strip().startswith("--config"):
        print("Config not implemented yet")
        sys.exit(0)
    elif command_list[1].strip().startswith("--"):
        print("Usage: nuisco <subcommand> [--args]")
        sys.exit(1)
    else: subcommand = command_list[1]
    #command_string = ' '.join(command_list[2:])
    struct_lst, others = seperate_pre_args(' '.join(command_list), {"nuisco": {"build": [], "create-template": ["ANY"], "help": []}})
    
    # Handling different sub-commands # use struct_lst from now on
    if struct_lst[1] == 'build': # Also define all_args aNd needed_args using the call stack
        func = getattr(build, 'build_main', None)
        if not func:
            raise ValueError(f"build_main function not found in build module") # list = list[str]
        kwargs = parse_args(command_string=others, all_args={"src": str, "out": str, "inLibs": list, "enablePlugins": list, "p": int, "extraArgs": list}, needed_args=["src", "out"])
        return func(**kwargs) # Call the function with unpacked arguments
    elif struct_lst[1] == 'create-template':
        if len(struct_lst) < 3:
            print("Usage: nuisco create-template [project_name] [--args]")
            raise ValueError("Project name is required for create-template")
        project_name = struct_lst[2]
        func = getattr(template, 'create_template', None)
        if not func:
            raise ValueError(f"create_template function not found in template module")
        kwargs = parse_args(command_string=others, all_args={"template_name": str, "pyversion": str, "github": bool, "install_requirements": bool}, needed_args=["template_name"])
        return func(project_name=project_name, **kwargs)
    elif struct_lst[1] == 'help':
        print("nuisco\n   -> build --src=./src --out=./out --arg=value\n   -> create-template [project_name] --template_name=ppt --arg=value\n   -> help")
        sys.exit(0)
    else:
        raise ValueError(f'Unknown subcommand: {struct_lst[1]}, type "nuisco help" for help.')

# Example usage
if __name__ == "__main__":
    command_line = ["nuisco", "create-template", "mypythonproject", "--template_name=ppt", "--github=True", "--install_requirements=True"]
    console_script(command_line)
