#!/bin/bash

echo "🚀 正在安裝 AccelBrainLauncher..."

# 檢查是否已安裝 pyinstaller
if ! command -v pyinstaller &> /dev/null; then
  echo "🔍 Can't detect pyinstaller，Try to install..."
  pip3 install pyinstaller || {
    echo "❌ Failed to install pyinstaller !"
    read -p "Press Enter to close..."
    exit 1
  }
else
  echo "✅ 已安裝 pyinstaller，略過安裝步驟"
fi

# 開始打包
pyinstaller launch.py --name AccelBrainLauncher --onefile --clean --distpath . || {
  echo "❌ 打包失敗，請檢查 launch.py 是否存在或是否有錯誤"
  read -p "按 Enter 關閉視窗..."
  exit 1
}
pyinstaller shut_down.py --name ShutDown --onefile --clean --distpath . || {
  echo "❌ 打包失敗，請檢查 shut_down.py 是否存在或是否有錯誤"
  read -p "按 Enter 關閉視窗..."
  exit 1
}
pyinstaller port_setting.py --name Setting --onefile --clean --distpath . || {
  echo "❌ 打包失敗，請檢查 port_setting.py 是否存在或是否有錯誤"
  read -p "按 Enter 關閉視窗..."
  exit 1
}
echo "✅ 打包完成！可執行 AccelBrainLauncher ShutDown Setting"
read -p "按 Enter 關閉視窗..."
