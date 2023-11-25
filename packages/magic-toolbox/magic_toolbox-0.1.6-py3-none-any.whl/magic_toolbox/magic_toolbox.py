from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction
from tools import (
                    create_project,
                    init,
                    add_function,
                    )
def get_tools() -> list[tuple[str,Callable]]:
    tools = import_module('tools')
    return [ (n,tool) 
            for n,tool in getmembers(tools) 
            if isfunction(tool)]
    
class MagicToolBox(object):
    
    """
    A CLI framework

    Raises:
        plac.Interpreter.Exit: [signals to exit interactive interpreter]
    """
    
 
    
    commands = 'create_project','init','add_function' 
    
    create_project = create_project
    init = init
    add_function = add_function
   

def main():
    Interpreter.call(MagicToolBox)
        
if __name__ == '__main__':
    main()