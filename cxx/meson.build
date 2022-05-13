project(
  'Personal Scripts', ['c', 'cpp'],
  version : '1.0.0',
  license : 'GPL3',
  default_options : [
    'cpp_std=c++23',
    'warning_level=3',
    'optimization=2',
    # 'werror=true',
    'prefix=/usr/local',
    'sysconfdir=/etc',
  ],
  meson_version : '>= 1.0.0'
)

bash = find_program('bash', required : true)
python = find_program('python3', required : true)

build_root = meson.project_build_root()
source_root = meson.project_source_root()

incdir = include_directories('src')

package = meson.project_name()
version = meson.project_version()
prefix = get_option('prefix')
bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
libdir = join_paths(prefix, get_option('libdir'), package)
sysconfdir = get_option('sysconfdir')
localedir = join_paths(prefix, get_option('localedir'))
mandir = join_paths(prefix, get_option('mandir'))

## compiler stuff

cc = meson.get_compiler('c')
cpp = meson.get_compiler('cpp')

# message(cc.get_id())
# message(cpp.get_id())

flags = []
link_flags = []

debug_flags = [
  '-ggdb3',

  '-pedantic',
  '-pedantic-errors',
  # '-Wfatal-errors',
  # '-ftime-trace',
]

if get_option('buildtype') == 'debug'
  flags += cpp.get_supported_arguments(debug_flags)
endif

release_flags = []

if get_option('buildtype') == 'release'
  flags += cpp.get_supported_arguments(release_flags)
endif

# Warnings

default_warning_flags = [
  '-Wconversion',
  '-Wchar-subscripts',
  '-Wcomment',
  '-Wdisabled-optimization',
  '-Wdouble-promotion',
  '-Wfloat-equal',
  '-Wformat=2',
  '-Wimplicit-fallthrough',
  '-Wimport',
  '-Winit-self',
  '-Wmissing-field-initializers',
  '-Wmissing-format-attribute',
  '-Wmissing-include-dirs',
  '-Wmissing-noreturn',
  '-Wparentheses',
  '-Wpointer-arith',
  '-Wsequence-point',
  '-Wshadow',
  '-Wsign-compare',
  '-Wstack-protector',
  '-Wstrict-aliasing',
  '-Wswitch',
  '-Wswitch-default',
  '-Wswitch-enum',
  '-Wtrigraphs',
  '-Wundef',
  '-Wuninitialized',
  '-Wunknown-pragmas',
  '-Wunreachable-code',
  '-Wunused',
  '-Wunused-function',
  '-Wunused-label',
  '-Wunused-parameter',
  '-Wunused-value',
  '-Wunused-result',
  '-Wunused-variable',
  '-Wunused-macros',
  '-Wvariadic-macros',
  '-Wvla',
  '-Wwrite-strings',
  '-Wignored-qualifiers',
  '-Wstring-compare',
  '-Walloca',
  '-Wdate-time',

  # Disabled Warnings
  # '-Wno-format-nonliteral',

  # Glibmm emits
  '-Wno-sign-conversion',

  # TODO
  # '-Wcast-qual',
]

flags += cpp.get_supported_arguments(default_warning_flags)

if cpp.has_multi_arguments('-Wformat', '-Werror=format-security')
  flags += '-Werror=format-security'
endif

# GCC only warning flags
if cpp.get_id() == 'gcc'
  default_warning_flags_gcc = [
    '-Wformat-overflow=2',
    '-Wformat-truncation',
    '-Warray-bounds=2',
    '-Warray-compare',
    '-Wzero-length-bounds',
    '-Wattribute-alias=2',
    '-Wduplicated-branches',
    '-Wduplicated-cond',
    '-Wtrampolines',
    '-Walloc-zero',
    '-Wstringop-overflow=4',

    # '-Weffc++',

    # Disabled Warnings
  ]

  flags += cpp.get_supported_arguments(default_warning_flags_gcc)
endif

# Clang only warning flags
if cpp.get_id() == 'clang'
  default_warning_flags_clang = [
    '-Wint-conversion',

    # Disabled Warnings
  ]

  flags += cpp.get_supported_arguments(default_warning_flags_clang)
endif

# Codegen

default_codegen_flags = [
  '-fwrapv',
  # '-fwrapv-pointer',
  '-ftrivial-auto-var-init=zero',
]

flags += cpp.get_supported_arguments(default_codegen_flags)

# Linker

if cpp.has_link_argument('-Wl,--as-needed')
  link_flags += '-Wl,--as-needed'
endif

noexecstack = false
if cpp.has_link_argument('-Wl,-z,noexecstack')
  link_flags += '-Wl,-z,noexecstack'
  noexecstack = true
endif

add_global_arguments(flags, language: ['c', 'cpp'])
add_global_link_arguments(link_flags, language: ['c', 'cpp'])

## dependencies

# ztd use system or subproject
ztd_dep = dependency('ztd', required : false)
if not ztd_dep.found() # using subproject
  ztd_proj = subproject('ztd', required : true)
  ztd_dep = ztd_proj.get_variable('ztd_dep')
endif

# magic_enum use system or subproject
magic_enum_dep = dependency('magic_enum', required : false)
if not magic_enum_dep.found() # using subproject
  magic_enum_proj = subproject('magic_enum', required : true)
  magic_enum_dep = magic_enum_proj.get_variable('magic_enum_dep')
endif

# toml11 use system or subproject
toml11_dep = dependency('toml11', required : false)
if not toml11_dep.found() # using subproject
  cmake = import('cmake')
  toml11_proj = cmake.subproject('toml11', required : true)
  toml11_dep = toml11_proj.dependency('toml11')
endif

# CLI11 use system or subproject
cli11_dep = dependency('CLI11', required : false)
if not cli11_dep.found() # using subproject
  cli11_dep_proj = subproject('cli11', required : true)
  cli11_dep_dep = cli11_dep_proj.get_variable('CLI11_dep')
endif

openssl_dep = dependency('openssl', required : true)

spdlog_dep = dependency('spdlog', required : true)
sigc_dep = dependency('sigc++-3.0', required : true)
pugixml_dep = dependency('pugixml', required : true)
nlohmann_json_dep = dependency('nlohmann_json', required : true)

# Gtk4 CPP
# gtkmm_dep = dependency('gtkmm-4.0', required : true)
glibmm_dep = dependency('glibmm-2.68', required : true)
giomm_dep = dependency('giomm-2.68', required : true)

dependencies = [
  # gtkmm_dep,
  glibmm_dep,
  giomm_dep,

  magic_enum_dep,
  toml11_dep,

  spdlog_dep,
  sigc_dep,
  pugixml_dep,
  nlohmann_json_dep,
  cli11_dep,

  openssl_dep,

  ztd_dep,
]

## preprocessor static

preprocessor = [
  # '-DGTK_DISABLE_DEPRECATED',
  # '-DGDK_DISABLE_DEPRECATED',

  # '-DGTKMM_DISABLE_DEPRECATED',
  # '-DGDKMM_DISABLE_DEPRECATED',
  '-DGLIBMM_DISABLE_DEPRECATED',
  '-DGIOMM_DISABLE_DEPRECATED',

  '-DZTD_VERSION=2',
]

foreach a : preprocessor
  add_project_arguments(a, language : ['c', 'cpp'])
endforeach

# Builds

# Used for all src files
target_type = 'executable'

