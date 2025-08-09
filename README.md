# LAN-Broadcast-Tool

## 完整项目结构

```
LAN-Broadcast-Tool/
├── main.py                  # 主程序代码
├── build_windows.bat        # Windows打包脚本
├── build_linux.sh           # Linux打包脚本
├── build.spec               # PyInstaller配置文件
├── icon.ico                 # 应用图标
├── requirements.txt         # 依赖库列表
└── README.md                # 项目说明
```

## requirements.txt 内容

```
PyQt5==5.15.7
pyinstaller==5.13.0
```

## 使用说明

### 在Windows上打包：
1. 双击运行`build_windows.bat`或执行`pyinstaller --onefile --windowed --name LANBroadcast --icon icon.ico main.py`
2. 生成的EXE文件位于`dist/LANBroadcast.exe`

### 在Linux上打包：
1. 给脚本添加执行权限：`chmod +x build_linux.sh`
2. 运行脚本：`./build_linux.sh`
3. 生成的二进制文件位于`dist/lan-broadcast`

## 注意事项

1. **跨平台问题**：
   - Windows打包需要在Windows系统上进行
   - Linux打包需要在Linux系统上进行
   - 无法在单个平台上打包所有平台的可执行文件

2. **依赖处理**：
   - PyInstaller会自动打包所有依赖
   - 对于复杂的依赖关系，可能需要手动添加隐藏导入

3. **文件大小**：
   - 打包后的文件会比较大（30-50MB），因为包含了Python解释器和所有依赖库
   - 可以使用UPX压缩减小文件大小（安装UPX并在PyInstaller中添加`--upx-dir`参数）

4. **防病毒软件**：
   - 某些防病毒软件可能会误报PyInstaller打包的文件
   - 如果遇到问题，请将可执行文件添加到防病毒软件的白名单

5. **运行时权限**：
   - 在Linux上，可能需要给二进制文件执行权限：`chmod +x lan-broadcast`
   - 应用需要网络权限才能发送/接收UDP消息
