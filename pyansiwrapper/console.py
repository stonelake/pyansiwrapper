import sys
import readline
import code
from pyansiwrapper import runner


adhoc = runner.ModuleAdHoc()
playadhoc = runner.PlayAdHoc()


def start_console():
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()


def start_ipython_console():
    from IPython import embed
    embed()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'ipython':
        start_ipython_console()
    else:
        start_console()
