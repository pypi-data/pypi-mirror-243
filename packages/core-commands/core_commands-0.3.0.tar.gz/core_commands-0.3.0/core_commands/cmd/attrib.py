from .command_cmd import command_cmd

def attrib(attribute,pathname = "",arguments = False,options = {
    "debug": False
}):
    """
    Display or change file attributes.
    """
    if(attribute):
        command_cmd(f"attrib {attribute} {pathname} {arguments}")