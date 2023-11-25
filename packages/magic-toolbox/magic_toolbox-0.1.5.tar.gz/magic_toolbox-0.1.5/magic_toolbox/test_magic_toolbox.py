from magic_cmd.run_cmd import run_cmd
from pathlib import Path
def test_create_project():
    run_cmd('python magic_toolbox.py create_project foo')
    foo = Path('foo')
    py = foo/'foo.py'
    tool = foo/'tools.py'
    assert foo.is_dir()
    assert py.exists()
    assert tool.exists()
    out = run_cmd('python foo/foo.py -h')
    assert '''
special commands
================
.last_tb

custom commands
===============
foo  help

''' in out
    run_cmd('rm -rf foo')
