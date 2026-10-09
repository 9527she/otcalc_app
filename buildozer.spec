[app]
title = 加班工资计算器
package.name = otcalc
package.domain = org.otcalc
source.dir = .
source.include_exts = py,json
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 32
android.ndk = 25
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1
