import subprocess
import sys

print("🚀 正在開始打包 AccelBrainLauncher（含 tkinter GUI）...\n")

# 自動安裝 pyinstaller（如果沒裝）
try:
    import PyInstaller
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

result = subprocess.call(
    [
        sys.executable,
        "-m",
        "PyInstaller",
        "launch.py",
        "--name",
        "AccelBrainLauncher",
        "--noconfirm",
        "--onefile",
        "--clean",
        "--distpath",
        ".",
    ]
)

if result == 0:
    print("\n✅ 打包完成！請執行 dist/AccelBrainLauncher.exe")
else:
    print("\n❌ 打包失敗，請檢查錯誤訊息")
