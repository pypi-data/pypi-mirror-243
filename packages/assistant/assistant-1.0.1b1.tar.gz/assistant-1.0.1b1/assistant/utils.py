from xonsh.built_ins import XSH


def get_kernel_interface():
    """
    Returns the kernel interface if it exists, otherwise returns None.
    """
    if hasattr(XSH.shell, "shell"):
        shell = XSH.shell.shell
        if hasattr(shell, "kernel_interface"):
            return XSH.shell.shell.kernel_interface
    return None

def get_spinner():
    """
    Returns the spinner from the kernel interface if it exists, otherwise returns None.
    """
    kernel_interface = get_kernel_interface()
    if kernel_interface and hasattr(kernel_interface, "spinner"):
        return kernel_interface.spinner
    return None

def say(text):
    """If spinner from kernel interface exists, use it to say text, otherwise print text.

    Args:
        text (str): The text to say.
    """
    spinner = get_spinner()
    if spinner:
        spinner.info(text)
    else:
        print(text)
