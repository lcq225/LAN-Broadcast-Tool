@echo off
echo ���ڰ�װ����...
rem pip install pyinstaller pyqt5

echo ���ڴ��WindowsӦ��...
pyinstaller --onefile --windowed --name LANBroadcast --icon icon.ico main.py

echo �����ɣ���ִ���ļ��� dist �ļ�����
pause