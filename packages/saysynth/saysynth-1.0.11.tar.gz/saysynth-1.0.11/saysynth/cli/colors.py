"""
Helpers for adding colored log output to the CLI.
<center><img src="/assets/img/spiral.png"></img></center>

"""
from click import style


def red(text):
    """
    Red text
    """
    return style(text, fg="red")


def green(text):
    """
    Green text
    """
    return style(text, fg="green")


def yellow(text):
    """
    Yellow text
    """
    return style(text, fg="yellow")


def blue(text):
    """
    Blue text
    """
    return style(text, fg="cyan")
