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

# Gtkmm4
gtkmm4_dep = dependency('gtkmm-4.0', required: true, version: '>=4.20.0')
glibmm4_dep = dependency('glibmm-2.68', required: true)
giomm4_dep = dependency('giomm-2.68', required: true)
sigc_dep = dependency('sigc++-3.0', required: true)

gtk4_dependencies = [
    gtkmm4_dep,
    glibmm4_dep,
    giomm4_dep,
    sigc_dep,
]

if false
  spdlog_dep = dependency('spdlog', required : true)
else
  cmake = import('cmake')
  # use std::format over bundled fmt::format
  cmake_opt_var = cmake.subproject_options()
  cmake_opt_var.add_cmake_defines({'SPDLOG_USE_STD_FORMAT': '1'})
  spdlog_proj = cmake.subproject('spdlog', required: true, options: cmake_opt_var)
  spdlog_dep = spdlog_proj.dependency('spdlog')
endif

# Logger static lib

logger_lib = static_library(
    'logger',
    files('logger/logger.cxx'),
    include_directories : include_directories('.'),
    dependencies : spdlog_dep,
    install: false,
)

logger_dep = declare_dependency(
    link_with : logger_lib,
    include_directories : include_directories('.'),
    dependencies : spdlog_dep,
)

# VFS static lib
vfs_dependencies = [
    gtk4_dependencies,
    logger_dep,
]

vfs_sources = files(
  'vfs/env.cxx',
  'vfs/error.cxx',
  'vfs/execute.cxx',
  'vfs/hash.cxx',
  'vfs/mouse.cxx',
  'vfs/proc.cxx',
  'vfs/recursion.cxx',
  'vfs/tools.cxx',
  'vfs/user-dirs.cxx',
)

vfs_lib = static_library(
    'vfs',
    vfs_sources,
    include_directories : include_directories('.'),
    dependencies : vfs_dependencies,
    install: false,
)

vfs_dep = declare_dependency(
    link_with : vfs_lib,
    include_directories : include_directories('.'),
    dependencies : vfs_dependencies,
)

# Builds

build_target(
  'chromium-default',
  sources: [
    'chromium-default.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'clean-downloads',
  sources: [
    'clean-downloads.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'count-filesize',
  sources: [
    'count-filesize.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'count-image',
  sources: [
    'count-image.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

install_symlink(
  'count-archive',
  install_dir: bindir,
  pointing_to: 'count-image',
)

install_symlink(
  'count-video',
  install_dir: bindir,
  pointing_to: 'count-image',
)

build_target(
  'digest-ebuild',
  sources: [
    'digest-ebuild.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'extract',
  sources: [
    'extract.cxx',
    'commandline/commandline.cxx',
    'utils/single-instance.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'snip',
  sources: [
    'snip.cxx',
    'commandline/commandline.cxx',
    'utils/single-instance.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'kernel-install-src',
  sources: [
    'kernel-install-src.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    vfs_dep,
  ],
)

build_target(
  'vulnerabilities',
  sources: [
    'vulnerabilities.cxx',
    'commandline/commandline.cxx',
  ],
  target_type: 'executable',
  include_directories: incdir,
  install: true,
  install_dir: bindir,
  dependencies: [
    logger_dep,
  ],
)
