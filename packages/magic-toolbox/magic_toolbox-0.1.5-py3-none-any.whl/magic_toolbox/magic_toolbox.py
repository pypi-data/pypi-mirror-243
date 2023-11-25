from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction


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
    
 
    
    commands = tuple(n for n,_ in get_tools()) 
   
for name,tool in get_tools():
    setattr(MagicToolBox,name,tool) 

def main():
    Interpreter.call(MagicToolBox)
        
if __name__ == '__main__':
    main()