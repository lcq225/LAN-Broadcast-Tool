@echo off
echo 正在安装依赖...
rem pip install pyinstaller pyqt5

echo 正在打包Windows应用...
pyinstaller --onefile --windowed --name LANBroadcast --icon icon.ico main.py

echo 打包完成！可执行文件在 dist 文件夹中
pause