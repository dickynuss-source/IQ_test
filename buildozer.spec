[app]
# (str) Title of your application
title = MathApp

# (str) Package name
package.name = mathappv1

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mathapp.game

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (str) Application versioning
version = 1.0

# ---------------------------
# Requirements
# ---------------------------
# Gunakan python3 plus versi Kivy yang stabil di p4a.
# Jika ingin versi Kivy lain, ganti di sini.
requirements = python3,kivy==2.1.0

# (list) Supported orientations
orientation = portrait

# (bool) fullscreen (0 = windowed, 1 = fullscreen)
fullscreen = 0

# (list) Permissions
# PENTING: Jangan aktifkan WRITE_EXTERNAL_STORAGE jika pakai user_data_dir
# Uncomment jika aplikasi butuh Internet:
# android.permissions = INTERNET

# ---------------------------
# Android settings
# ---------------------------
# Target Android API (set cukup tinggi agar kompatibel)
android.api = 33
# Minimum API
android.minapi = 21
# Use private storage (true = lebih aman, tidak perlu permission)
android.private_storage = True
# Auto accept SDK licenses to avoid interactive prompt
android.accept_sdk_license = True

# Build archs - tetapkan kedua agar berjalan di perangkat 32 & 64 bit
android.archs = arm64-v8a, armeabi-v7a

# Enable Android backup (optional)
android.allow_backup = True

# Build artifact format
# Untuk testing/debug lebih gampang pakai apk — ubah ke aab bila mau rilis ke Play Store
android.release_artifact = apk
android.debug_artifact = apk

# Python for android (p4a) specific
p4a.branch = master
p4a.bootstrap = sdl2

# (Optional) Set a specific NDK version if kamu pernah mengalami masalah NDK.
# Contoh (commented): android.ndk = 23b

# iOS settings (tidak dipakai di Android)
ios.kivy_ios_dir = ../kivy-ios
ios.codesign.allowed = false

[buildozer]
# Log level (0 error only, 1 info, 2 debug)
log_level = 2
warn_on_root = 1

# (Optional) Jika mau output lebih kecil / build caching, ada opsi tambahan,
# tapi untuk permulaan jangan diubah supaya build lebih prediktabel.
