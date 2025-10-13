project(
  'Personal Scripts', ['c', 'cpp'],
  version : '1.0.0',
  license : 'GPL3',
  default_options : [
    'c_std=c23',
    'cpp_std=c++26',
    'buildtype=debugoptimized',
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

incdir = include_directories('cxx')

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

if get_option('buildtype') == 'debug' or get_option('buildtype') == 'debugoptimized'
    flags += cpp.get_supported_arguments([
        '-ggdb3',
        '-pedantic',
        '-pedantic-errors',
        '-fno-omit-frame-pointer',
        '-mno-omit-leaf-frame-pointer',
        '-fasynchronous-unwind-tables',
        # '-ftime-trace',
        # '-fsave-optimization-record',

        # '-Werror',
        '-Wfatal-errors',
    ])
endif

if get_option('buildtype') == 'release'
    flags += cpp.get_supported_arguments([])
endif

# Default
flags += cpp.get_supported_arguments([
    '-fexceptions',

    '-finput-charset=UTF-8',
    '-fexec-charset=UTF-8',

    '-fno-delete-null-pointer-checks',
    '-fno-strict-aliasing',
    '-fno-strict-overflow',

    '-ftrivial-auto-var-init=zero',
    '-fzero-init-padding-bits=all',
])

# Hardening
flags += cpp.get_supported_arguments([
    '-Wformat=2',
    '-Wformat-overflow=2',
    '-Wformat-truncation',
    '-Werror=format-security',

    '-fstack-protector-strong',
    '-fstack-clash-protection',
    '-fcf-protection=full',

    '-Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3',

    # GCC libstdc++
    # '-Wp,-D_GLIBCXX_DEBUG',
    '-Wp,-D_GLIBCXX_ASSERTIONS',

    # LLVM libc++
    # '-Wp,-D_LIBCPP_ASSERT',
    # '-Wp,-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST',
])

# Warnings
flags += cpp.get_supported_arguments([
    '-Walloca',
    '-Walloc-zero',
    '-Warray-bounds=2',
    '-Warray-compare',
    '-Wattribute-alias=2',
    '-Wbidi-chars=any',
    '-Wcast-align',
    '-Wcast-qual',
    '-Wchar-subscripts',
    '-Wcomment',
    '-Wconversion',
    '-Wdate-time',
    '-Wdisabled-optimization',
    '-Wdouble-promotion',
    '-Wduplicated-branches',
    '-Wduplicated-cond',
    # '-Wextra-semi', // TODO warnings from glibmm
    '-Wfloat-equal',
    '-Wignored-qualifiers',
    '-Wimplicit-fallthrough',
    '-Wimport',
    '-Winit-self',
    '-Wint-conversion',
    '-Wmissing-field-initializers',
    '-Wmissing-format-attribute',
    '-Wmissing-include-dirs',
    '-Wmissing-noreturn',
    '-Wnon-virtual-dtor',
    '-Wnull-dereference',
    # '-Wold-style-cast', // TODO warnings from glibmm
    '-Woverloaded-virtual',
    '-Wparentheses',
    '-Wpointer-arith',
    '-Wsequence-point',
    '-Wshadow',
    '-Wsign-compare',
    '-Wsign-conversion',
    '-Wstack-protector',
    '-Wstrict-aliasing',
    '-Wstring-compare',
    '-Wstringop-overflow=4',
    '-Wswitch',
    '-Wswitch-enum',
    '-Wtrampolines',
    '-Wtrigraphs',
    '-Wundef',
    '-Wuninitialized',
    '-Wunknown-pragmas',
    '-Wunreachable-code',
    '-Wunused',
    '-Wunused-function',
    '-Wunused-label',
    '-Wunused-macros',
    '-Wunused-parameter',
    '-Wunused-result',
    '-Wunused-value',
    '-Wunused-variable',
    '-Wvariadic-macros',
    '-Wvla',
    '-Wwrite-strings',
    '-Wzero-length-bounds',
])

# Disabled Warnings
flags += cpp.get_supported_arguments([])

# Disabled GCC Warnings
if cpp.get_id() == 'gcc'
    flags += cpp.get_supported_arguments([])
endif

# Disabled Clang Warnings
if cpp.get_id() == 'clang'
    flags += cpp.get_supported_arguments([])
endif

# Linker

link_flags = []
link_flags += cpp.get_supported_link_arguments([
    '-Wl,-O1',
    '-Wl,--as-needed',
    '-Wl,--sort-common',
    '-Wl,-z,relro',
    '-Wl,-z,now',
    '-Wl,-z,pack-relative-relocs',
    '-Wl,-z,noexecstack',
    '-Wl,-z,defs',
])

add_global_arguments(flags, language: ['c', 'cpp'])
add_global_link_arguments(link_flags, language: ['c', 'cpp'])

## preprocessor static

preprocessor = [
  # '-DGTK_DISABLE_DEPRECATED',
  # '-DGDK_DISABLE_DEPRECATED',

  # '-DGTKMM_DISABLE_DEPRECATED',
  # '-DGDKMM_DISABLE_DEPRECATED',
  '-DGLIBMM_DISABLE_DEPRECATED',
  '-DGIOMM_DISABLE_DEPRECATED',

  # '-DZTD_SAFE_NUMERICS_TYPES',
]

foreach a : preprocessor
  add_project_arguments(a, language : ['c', 'cpp'])
endforeach

subdir('cxx')

# hangs when running install
# meson.add_install_script('./tools_bin_setup.py')
# meson.add_install_script('./tools_symlink_chrome.py')
