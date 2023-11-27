from subprocess import run

def command_cmd(command_):
        #TODO: deberia verificar que si el sistema es windows.
        return run(f'{command_}',shell=True)