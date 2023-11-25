project('ivlam', 'c',
  version : '0.1',
  meson_version: '>=0.64.0',
  default_options : ['warning_level=2'],
)

add_languages('fortran')

fortran_compiler = meson.get_compiler('fortran')

if fortran_compiler.get_id() == 'gcc'
  add_project_arguments('-O3', '-g', '-ffree-line-length-none', language: 'fortran')
elif fortran_compiler.get_id() == 'intel'
  add_project_arguments('-O3', '-g', '-extend-source', language: 'fortran')
elif fortran_compiler.get_id() == 'pgi'
  add_project_arguments('-O3', '-g', '-Mextend', language: 'fortran')
endif

subdir('src')