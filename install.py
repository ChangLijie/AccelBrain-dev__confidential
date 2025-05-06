import subprocess

result = subprocess.call(["bash", "./install.sh"])

if result == 0:
    print("\n✅ 打包完成！請執行 AccelBrainLauncher")
else:
    print("\n❌ 打包失敗，請檢查錯誤訊息")
