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

## dependencies

# ztd use system or subproject
ztd_dep = dependency('ztd', required : false)
if not ztd_dep.found() # using subproject
  ztd_proj = subproject('ztd', required : true)
  ztd_dep = ztd_proj.get_variable('ztd_dep')
endif

# magic_enum use system or subproject
magic_enum_dep = dependency('magic_enum', required : false, version: '>=0.9.7')
if not magic_enum_dep.found() # using subproject
  magic_enum_proj =  dependency('magic_enum', required: true, version: '>=0.9.7')
  magic_enum_dep = magic_enum_proj.get_variable('magic_enum_dep')
endif

# CLI11 use system or subproject
cli11_dep = dependency('CLI11', required : false)
if not cli11_dep.found() # using subproject
  cli11_dep_proj = subproject('cli11', required : true)
  cli11_dep_dep = cli11_dep_proj.get_variable('CLI11_dep')
endif

spdlog_dep = dependency('spdlog', required : true)
sigc_dep = dependency('sigc++-3.0', required : true)

# Gtk4 CPP
gtkmm_dep = dependency('gtkmm-4.0', required : true)
glibmm_dep = dependency('glibmm-2.68', required : true)
# giomm_dep = dependency('giomm-2.68', required : true)

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

# Builds

# chromium-default
build_target(
  'chromium-default',
  sources: [
    'cxx/chromium-default.cxx',

    'cxx/lib/env.cxx',
    'cxx/lib/commandline.cxx',
    'cxx/lib/user-dirs.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# clean-downloads
build_target(
  'clean-downloads',
  sources: [
    'cxx/clean-downloads.cxx',

    'cxx/lib/commandline.cxx',
    'cxx/lib/hash.cxx',
    'cxx/lib/user-dirs.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# digest-ebuild
build_target(
  'digest-ebuild',
  sources: [
    'cxx/digest-ebuild.cxx',

    'cxx/lib/commandline.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# extract
build_target(
  'extract',
  sources: [
    'cxx/extract.cxx',

    'cxx/lib/commandline.cxx',
    'cxx/lib/env.cxx',
    'cxx/lib/proc.cxx',
    'cxx/lib/single-instance.cxx',
    'cxx/lib/user-dirs.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# snip
build_target(
  'snip',
  sources: [
    'cxx/snip.cxx',

    'cxx/lib/commandline.cxx',
    'cxx/lib/env.cxx',
    'cxx/lib/proc.cxx',
    'cxx/lib/single-instance.cxx',
    'cxx/lib/user-dirs.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# snip
build_target(
  'kernel-install-src',
  sources: [
    'cxx/kernel-install-src.cxx',

    'cxx/lib/commandline.cxx',
    'cxx/lib/env.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    glibmm_dep,
    spdlog_dep,
    ztd_dep,
  ],
)

# vulnerabilities
build_target(
  'vulnerabilities',
  sources: [
    'cxx/vulnerabilities.cxx',

    'cxx/lib/commandline.cxx',

    'cxx/logger/logger.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    spdlog_dep,
    ztd_dep,
  ],
)

meson.add_install_script('./tools_bin_setup.py')
meson.add_install_script('./tools_symlink_chrome.py')
