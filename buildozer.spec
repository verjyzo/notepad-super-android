[app]
title = Notepad Pro
package.name = notepadpro
package.domain = org.pribadi
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy

# Izin akses penyimpanan internal HP agar bisa membaca .srt dan .txt
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

# FOKUS PADA HP MODERN (Mempercepat build & menghindari error arsitektur lama)
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
