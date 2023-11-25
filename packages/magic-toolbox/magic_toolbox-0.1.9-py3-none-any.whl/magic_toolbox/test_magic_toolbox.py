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
    assert '''special commands
================
.last_tb

custom commands
===============
foo  help
''' in out
    from os import chdir
    chdir(foo:=Path('foo'))
    run_cmd('python ../magic_toolbox.py add_function bar')
    out = run_cmd('python foo.py bar -h')
    assert 'usage: foo.py bar [-h]' in out
    chdir(foo.parent)
    run_cmd('rm -rf foo')
