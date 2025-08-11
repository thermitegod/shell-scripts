build_target(
  'chromium-default',
  sources: [
    'chromium-default.cxx',
    'commandline/commandline.cxx',
    'vfs/env.cxx',
    'vfs/execute.cxx',
    'vfs/user-dirs.cxx',
    'logger/logger.cxx',
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

build_target(
  'clean-downloads',
  sources: [
    'clean-downloads.cxx',
    'commandline/commandline.cxx',
    'vfs/execute.cxx',
    'vfs/hash.cxx',
    'vfs/user-dirs.cxx',
    'logger/logger.cxx',
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

build_target(
  'count-filesize',
  sources: [
    'count-filesize.cxx',
    'commandline/commandline.cxx',
    'vfs/execute.cxx',
    'vfs/recursion.cxx',
    'logger/logger.cxx',
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

build_target(
  'digest-ebuild',
  sources: [
    'digest-ebuild.cxx',
    'commandline/commandline.cxx',
    'vfs/execute.cxx',
    'logger/logger.cxx',
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

build_target(
  'extract',
  sources: [
    'extract.cxx',
    'commandline/commandline.cxx',
    'utils/single-instance.cxx',
    'vfs/env.cxx',
    'vfs/error.cxx',
    'vfs/execute.cxx',
    'vfs/proc.cxx',
    'vfs/user-dirs.cxx',
    'logger/logger.cxx',
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

build_target(
  'snip',
  sources: [
    'snip.cxx',
    'commandline/commandline.cxx',
    'utils/single-instance.cxx',
    'vfs/env.cxx',
    'vfs/error.cxx',
    'vfs/execute.cxx',
    'vfs/proc.cxx',
    'vfs/user-dirs.cxx',

    'logger/logger.cxx',
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

build_target(
  'kernel-install-src',
  sources: [
    'kernel-install-src.cxx',
    'commandline/commandline.cxx',
    'vfs/env.cxx',
    'vfs/execute.cxx',
    'logger/logger.cxx',
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

build_target(
  'vulnerabilities',
  sources: [
    'vulnerabilities.cxx',
    'commandline/commandline.cxx',
    'logger/logger.cxx',
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
