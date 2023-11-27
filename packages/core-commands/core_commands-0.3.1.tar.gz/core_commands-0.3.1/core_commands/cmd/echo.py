from command_cmd import command_cmd

def echo(text = False,arguments = False):
    """
    Display messages on screen, turn command-echoing on or off.

    arguments: ON | OFF | /?
    """
    if (text):
        return command_cmd(f'echo {text}')
    if (arguments):
        return command_cmd(f'echo {arguments}')
    if (text and arguments):
        return command_cmd(f'echo {text} {arguments}')
    return command_cmd("echo")
