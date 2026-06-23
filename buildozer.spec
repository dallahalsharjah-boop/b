[app]
title = Widget
package.name = abdullahnasser
package.domain = com.widget
source.dir = .
source.include_exts = py,png,jpg,ttf,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,arabic-reshaper,python-bidi,hijridate
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = armeabi-v7a
android.allow_backup = False
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
