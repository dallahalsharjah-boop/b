[app]

# ── App info ──────────────────────────────────
title           = By.Abdullah NassEr
package.name    = abdullahnasser
package.domain  = com.widget

source.dir      = .
source.include_exts = py,png,jpg,ttf,kv,atlas

version         = 1.0

# ── Python requirements ───────────────────────
# All packages needed inside the APK
requirements = python3,kivy==2.3.0,arabic-reshaper,python-bidi,hijridate

# ── Orientation & display ─────────────────────
orientation = portrait
fullscreen  = 0

# ── Android settings ──────────────────────────
android.permissions     = INTERNET
android.api             = 33
android.minapi          = 21
android.sdk             = 33
android.ndk             = 25b
android.ndk_api         = 21
android.archs           = arm64-v8a, armeabi-v7a
android.allow_backup    = False

# App icon (place a 512x512 PNG named icon.png in the folder)
# icon.filename = %(source.dir)s/icon.png

# ── iOS (unused) ──────────────────────────────
[buildozer]
log_level = 2
warn_on_root = 1
