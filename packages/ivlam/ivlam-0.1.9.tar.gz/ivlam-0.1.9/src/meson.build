py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy, incdir_f2py)

_ivlam_source = custom_target('_ivlammodule',
  input : ['ivlam.pyf','.f2py_f2cmap'],
  output : ['_ivlammodule.c', '_ivlam-f2pywrappers.f'],
  command : [py, '-m', 'numpy.f2py', '@INPUT0@', '--f2cmap','@INPUT1@','--build-dir', 'src','--lower']
)
py.extension_module('_ivlam',
  ['ivlam/ivLamRuntimeV2p41_738416p65617.f90', _ivlam_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  install : true,
  subdir: 'ivlam'
)
py.install_sources(['__init__.py','ivlam.py','ivlam/ivLamTree_20210202_160219_i2d8.bin'],subdir: 'ivlam')