import sys
import socket
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

# 获取本机IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# 获取广播地址
def get_broadcast_address():
    try:
        local_ip = get_local_ip()
        parts = local_ip.split('.')
        parts[-1] = '255'
        return '.'.join(parts)
    except:
        return "255.255.255.255"

class UdpReceiver(QObject):
    message_received = pyqtSignal(str)
    
    def __init__(self, port=9999):
        super().__init__()
        self.port = port
        self.running = False
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.running = False
        try:
            # 创建一个临时socket来唤醒接收线程
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b"exit", ("127.0.0.1", self.port))
            s.close()
        except:
            pass
        
    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        try:
            sock.bind(("0.0.0.0", self.port))
            
            while self.running:
                try:
                    data, addr = sock.recvfrom(4096)
                    if data == b"exit":
                        break
                    message = data.decode("utf-8")
                    display_msg = f"[来自 {addr[0]}] {message}"
                    self.message_received.emit(display_msg)
                except Exception as e:
                    print(f"接收错误: {e}")
        finally:
            sock.close()

class BroadcastApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("局域网UDP消息广播工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QGroupBox {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit, QTextEdit {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """)
        
        # 初始化变量
        self.local_ip = get_local_ip()
        self.broadcast_address = get_broadcast_address()
        self.port = 9999
        self.receiver = None
        
        self.init_ui()
        
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # 标题
        title = QLabel("局域网UDP消息广播工具")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #3498db; margin: 20px 0;")
        
        # 网络信息组
        network_group = QGroupBox("网络信息")
        network_layout = QVBoxLayout()
        
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("本机IP地址:"))
        self.ip_label = QLabel(self.local_ip)
        ip_layout.addWidget(self.ip_label)
        ip_layout.addStretch()
        
        broadcast_layout = QHBoxLayout()
        broadcast_layout.addWidget(QLabel("广播地址:"))
        self.broadcast_label = QLabel(self.broadcast_address)
        broadcast_layout.addWidget(self.broadcast_label)
        broadcast_layout.addStretch()
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口:"))
        self.port_edit = QLineEdit(str(self.port))
        self.port_edit.setMaximumWidth(100)
        port_layout.addWidget(self.port_edit)
        port_layout.addStretch()
        
        network_layout.addLayout(ip_layout)
        network_layout.addLayout(broadcast_layout)
        network_layout.addLayout(port_layout)
        network_group.setLayout(network_layout)
        
        # 消息发送组
        send_group = QGroupBox("发送消息")
        send_layout = QVBoxLayout()
        
        self.message_edit = QLineEdit()
        self.message_edit.setPlaceholderText("输入要广播的消息...")
        
        send_button = QPushButton("广播消息")
        send_button.clicked.connect(self.send_message)
        
        send_layout.addWidget(self.message_edit)
        send_layout.addWidget(send_button)
        send_group.setLayout(send_layout)
        
        # 消息接收组
        receive_group = QGroupBox("接收消息")
        receive_layout = QVBoxLayout()
        
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setFont(QFont("Arial", 10))
        
        receive_buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("开始接收")
        self.start_button.clicked.connect(self.start_receiving)
        self.stop_button = QPushButton("停止接收")
        self.stop_button.clicked.connect(self.stop_receiving)
        self.stop_button.setEnabled(False)
        self.clear_button = QPushButton("清空记录")
        self.clear_button.clicked.connect(self.clear_messages)
        
        receive_buttons_layout.addWidget(self.start_button)
        receive_buttons_layout.addWidget(self.stop_button)
        receive_buttons_layout.addWidget(self.clear_button)
        
        receive_layout.addWidget(self.message_display)
        receive_layout.addLayout(receive_buttons_layout)
        receive_group.setLayout(receive_layout)
        
        # 状态栏
        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("color: #bdc3c7; padding: 5px;")
        
        # 添加到主布局
        main_layout.addWidget(title)
        main_layout.addWidget(network_group)
        main_layout.addWidget(send_group)
        main_layout.addWidget(receive_group)
        main_layout.addWidget(self.status_label)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def send_message(self):
        message = self.message_edit.text().strip()
        if not message:
            QMessageBox.warning(self, "输入错误", "请输入要发送的消息")
            return
            
        try:
            port = int(self.port_edit.text())
        except ValueError:
            QMessageBox.warning(self, "端口错误", "端口号必须是整数")
            return
            
        try:
            # 创建UDP套接字
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # 发送消息
            sock.sendto(message.encode("utf-8"), (self.broadcast_address, port))
            sock.close()
            
            # 在本地显示
            self.display_message(f"[我发送的] {message}")
            self.status_label.setText(f"消息已广播到 {self.broadcast_address}:{port}")
            self.message_edit.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "发送错误", f"发送消息时出错: {str(e)}")
            
    def start_receiving(self):
        try:
            port = int(self.port_edit.text())
        except ValueError:
            QMessageBox.warning(self, "端口错误", "端口号必须是整数")
            return
            
        if self.receiver is not None:
            self.stop_receiving()
            
        self.receiver = UdpReceiver(port)
        self.receiver.message_received.connect(self.display_message)
        self.receiver.start()
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText(f"正在监听端口 {port}...")
        
    def stop_receiving(self):
        if self.receiver:
            self.receiver.stop()
            self.receiver = None
            
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("已停止监听")
        
    def display_message(self, message):
        self.message_display.append(message)
        self.message_display.verticalScrollBar().setValue(
            self.message_display.verticalScrollBar().maximum()
        )
        
    def clear_messages(self):
        self.message_display.clear()
        
    def closeEvent(self, event):
        self.stop_receiving()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(44, 62, 80))
    palette.setColor(QPalette.WindowText, QColor(236, 240, 241))
    app.setPalette(palette)
    
    window = BroadcastApp()
    window.show()
    sys.exit(app.exec_())