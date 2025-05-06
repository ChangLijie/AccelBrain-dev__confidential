#!/bin/bash

echo "🚀 Installing ENV..."

# Check and install required APT packages
try_apt() {
  local pkg=$1
  echo "🔧 Checking if APT package '$pkg' is installed..."
  if ! dpkg -s "$pkg" &> /dev/null; then
    echo "📦 '$pkg' is not installed. Installing..."
    sudo apt-get update && sudo apt-get install -y "$pkg" || {
      echo "❌ Failed to install '$pkg'!"
      read -p "Press Enter to close..."
      exit 1
    }
  else
    echo "✅ '$pkg' is already installed"
  fi
}

# Check and install required Python modules
try_pip() {
  local module=$1
  echo "🔧 Checking if Python module '$module' is installed..."
  python3 -c "import $module" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "📦 '$module' is not installed. Installing via pip..."
    pip3 install "$module" || {
      echo "❌ Failed to install Python module '$module'!"
      read -p "Press Enter to close..."
      exit 1
    }
  else
    echo "✅ Python module '$module' is already installed"
  fi
}

# Ensure required dependencies are installed
try_apt "python3-tk"
try_apt "unifont"
try_pip "yaml"

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null; then
  echo "🔍 'pyinstaller' not found. Installing..."
  pip3 install pyinstaller || {
    echo "❌ Failed to install 'pyinstaller'!"
    read -p "Press Enter to close..."
    exit 1
  }
else
  echo "✅ 'pyinstaller' is already installed"
fi
echo "🚀 Build AccelBrainLauncher..."

# Start building executables
pyinstaller launch.py --name AccelBrainLauncher --onefile --clean --distpath . || {
  echo "❌ Failed to build AccelBrainLauncher. Check launch.py for issues."
  read -p "Press Enter to close..."
  exit 1
}

echo "🚀 Build AccelBrainShutDown..."

pyinstaller shut_down.py --name AccelBrainShutDown --onefile --clean --distpath . || {
  echo "❌ Failed to build ShutDown. Check shut_down.py for issues."
  read -p "Press Enter to close..."
  exit 1
}

echo "🚀 Build AccelBrainSetting..."
pyinstaller port_setting.py --name AccelBrainSetting --onefile --clean --distpath . || {
  echo "❌ Failed to build Setting. Check port_setting.py for issues."
  read -p "Press Enter to close..."
  exit 1
}

echo "✅ Build complete! You can now run AccelBrainLauncher, AccelBrainShutDown, and AccelBrainSetting"
read -p "Press Enter to close..."
