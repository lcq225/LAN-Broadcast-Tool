#!/bin/bash
echo "正在安装依赖..."
pip install pyinstaller pyqt5

echo "正在打包Linux应用..."
pyinstaller --onefile --name lan-broadcast --windowed main.py

echo "打包完成！可执行文件在 dist 文件夹中"