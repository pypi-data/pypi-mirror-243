from pathlib import Path

def create_project(self,name:('The name of project','positional')):
    '''
    Creates a plac cli project.
    '''
    project= Path(name)
    if name:
        if project.exists():
            raise Exception(f'{name} already exists!')
        project.mkdir()
    tools = project/'tools.py'
    if tools.exists():
        raise Exception(f'{name} already exists!')
    tools.write_text(f"""def {name}(self,):
    '''
    This is just a dummy sub command to use as an example.
    You can use this as help message.
    '''
    """)
    cli:Path = project / f'{name}.py'
    class_name = name.capitalize()
    cli.write_text(f"""from plac import Interpreter
from typing import Callable
from importlib import import_module
from inspect import getmembers, isfunction


def get_tools() -> list[tuple[str,Callable]]:
    tools = import_module('tools')
    return [ (n,tool) 
            for n,tool in getmembers(tools) 
            if isfunction(tool)]
    
class {class_name}(object):
    
    commands = tuple(n for n,_ in get_tools()) 
   
for name,tool in get_tools():
    setattr({class_name},name,tool) 
        
if __name__ == '__main__':
    Interpreter.call({class_name})
    """)
    print(f'Created {name}/{name}.py and {name}/tools.py')
    
def add_function(self,name:('The name of function','positional')):
    '''
    This creates a new function in toolbox.tools
    '''
    tools = Path('tools.py')
    if not tools.exists():
        raise Exception('No toolbox.tools run magic_toolbox init')
    new_function:str=f"""def {name}(self):
    '''
    Put your doc string here
    '''
    """
    tool_box = tools.read_text()
    tool_box = '\n'.join([tool_box,'',new_function])
    tools.write_text(tool_box)
    print('added:\n',new_function)


def init(self):
    '''
    Add tool.toolbox to this directory.
    '''
    tools:Path = Path('tools.py')
    if tools.exists():
        raise Exception('tools.py already exists')
    create_project(self, '') 