import os, sys
import io
import traceback
# import builtins
import subprocess
import contextlib

from xonsh.built_ins import XSH

from assistant.parser import ParseResult


def _convert_to_xonsh_subproc_string(parse: ParseResult):
    out = [[]]
    WORDS_THAT_SHOULD_BE_ALONE = ("|", ">>", ">", "<", "<<", "&&", "||")
    for word in parse.words:
        if word in WORDS_THAT_SHOULD_BE_ALONE:
            out.append(word)
            out.append([])
        else:
            out[-1].append(word)

    return out


HOME = os.environ.get("HOME", "~")


def clear(intro=None):
    os.system("clear")
    if intro:
        print(intro)
    return intro


def user_input_match_builtin_commands(input_text):
    # match builtin commands
    lowercase_input_text = input_text.lower()
    if lowercase_input_text == "exit":
        # What is the exit code of a sell when it is exited with exit?
        exit(0)
    elif lowercase_input_text == "clear":
        return clear()
    elif lowercase_input_text.split()[0] == "help":
        return "To get help, ask Assistant."
    # elif os.path.exists(input_text) and os.path.isfile(input_text):
    #     print(f"cat {input_text}")
    #     try:
    #         with open(input_text) as f:
    #             return f.read()
    #     except FileNotFoundError:
    #         return f"You want to read a file but there is no such file named {input_text}."
    #     except Exception as e:
    #         return e
    #         return None
    elif os.path.exists(input_text) and os.path.isdir(input_text):
        print(f"cd {input_text}")
        try:
            os.chdir(input_text.split()[0])
            return f"Welcome in `{os.getcwd().replace(HOME, '~')}`!"
        except FileNotFoundError:
            return f"This is wiered and should have never happend.\n{input_text.split()[1]} is a directory that existed a second ago but it does not anymore.\nI am deeply sorry for this. Whithout a proper destination, I can't change directory."
        except Exception as e:
            return e
            return None
    elif input_text.lower().split()[0] == "cd":
        try:
            os.chdir(input_text.split()[1])
            return f"Welcome in `{os.getcwd().replace(HOME, '~')}`!"
        except FileNotFoundError:
            return f"You want to change directory but there is no such file or directory named {input_text.split()[1]}."
        except Exception as e:
            return e
            return None
    # elif input_text.lower().split()[0] == "ls":
    #     try:
    #         target_dir = input_text.split()[1] if len(input_text.split()) > 1 else "."
    #         list_dir = os.listdir(target_dir)
    #         return "\n".join([f"- `{f}`" for f in list_dir])
    #     except FileNotFoundError:
    #         return f"You want to list files in a directory but there is no such file or directory named {target_dir}."
    #     except Exception as e:
    #         return e


# def execute_user_input(input_text):
#     output = None
#     try:
#         output = eval(input_text, globals())
#     except Exception as eval_e:
#         try:
#             # Attempt to execute the input text as Python code
#             with io.StringIO() as buf, \
#             contextlib.redirect_stdout(buf):#, \
#             # contextlib.redirect_stderr(buf):
#                 exec(input_text, globals())
#                 output = buf.getvalue().strip()
#             return output
#         except (SyntaxError, NameError) as exec_e:
#             output = None
#         except Exception as exec_e:
#             output = exec_e

#     return output

def execute_user_input(input_text):
    output = None

    try:
        # Try to execute the input as Python code using eval
        output = str(eval(input_text, globals()))
    except Exception as eval_e:
        try:
            # Attempt to execute the input text as Python code using exec
            with io.StringIO() as buf, \
            contextlib.redirect_stdout(buf):
                exec(input_text, globals())
                output = buf.getvalue().strip()
        except (SyntaxError, NameError):
            output = None
        except Exception as exec_e:
            output = str(exec_e)

    return output

def os_system_user_input(input_text):
    try:
        # Attempt to execute the input text as a shell command
        shell_result = subprocess.run(
            input_text,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the shell command executed successfully
        if shell_result.returncode == 0:
            return shell_result.stdout.strip()
        elif shell_result.returncode == 127:
            # If the shell command is not found, return None
            return None
        elif shell_result.returncode in [1, 2]:
            return None
        else:
            return str(
                f"{input_text.split()[0]}: Exiting with error {shell_result.stderr}; code {shell_result.returncode}"
            )
    except subprocess.CalledProcessError as sh_exec_e:
        return f"{input_text}: {sh_exec_e}"


def execute(command: str):
    output = None

    if command in ["", " ", "\n", "\t", "\r", None]:
        return output
    output = user_input_match_builtin_commands(command)
    if output:
        return output
    output = execute_user_input(command)
    if output:
        return output
    # elif logs:
    #     return "\n".join(logs)
    output = os_system_user_input(command)
    return output


if __name__ == "__main__":
    while True:
        command = input(">>> ")
        print(execute(command))
