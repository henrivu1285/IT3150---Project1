import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QLabel, QFileDialog, QMessageBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from huffman import Huffman

class HuffmanApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Huffman File Compress")
        self.setGeometry(100, 100, 500, 380)
        self.current_file_path = None 

        # Kéo thả file
        self.setAcceptDrops(True) 

        # Giao diện chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Tiêu đề
        self.title_label = QLabel("Huffman Compress")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.title_label)

        # Khu vực hiển thị file 
        self.file_info_frame = QFrame()
        self.file_info_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 8px; padding: 20px;")
        info_layout = QVBoxLayout(self.file_info_frame)
        
        self.lbl_instruction = QLabel("Kéo thả file vào đây\nhoặc bấm nút bên dưới")
        self.lbl_instruction.setAlignment(Qt.AlignCenter)
        self.lbl_instruction.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        info_layout.addWidget(self.lbl_instruction)
        
        layout.addWidget(self.file_info_frame)

        # Nút chọn file
        self.btn_browse = QPushButton("📂 Chọn File")
        self.btn_browse.setCursor(Qt.PointingHandCursor)
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; padding: 10px; 
                border-radius: 5px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_browse.clicked.connect(self.browse_file)
        layout.addWidget(self.btn_browse)

        # Khu vực nút hành động
        action_layout = QVBoxLayout()
        
        self.btn_compress = QPushButton("Nén File (.bin)")
        self.btn_compress.setCursor(Qt.PointingHandCursor)
        # Thêm style cho trạng thái disabled để người dùng dễ nhận biết
        self.btn_compress.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 10px; 
                border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #219150; }
            QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; } 
        """)
        self.btn_compress.clicked.connect(self.run_compress)
        self.btn_compress.setEnabled(False) 
        action_layout.addWidget(self.btn_compress)

        self.btn_decompress = QPushButton("Giải nén File (.txt)")
        self.btn_decompress.setCursor(Qt.PointingHandCursor)
        self.btn_decompress.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white; padding: 10px; 
                border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #d35400; }
            QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }
        """)
        self.btn_decompress.clicked.connect(self.run_decompress)
        self.btn_decompress.setEnabled(False) 
        action_layout.addWidget(self.btn_decompress)

        layout.addLayout(action_layout)
        layout.addStretch()

    # Logic kéo thả
    def dragEnterEvent(self, event):
        # Khi kéo file vào, chấp nhận sự kiện
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Khi thả file ra
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            # Lấy file đầu tiên (nếu kéo nhiều file)
            filepath = files[0]
            self.process_file_selection(filepath)

    # Các hàm xử lý

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Chọn file", "", "All Files (*)")
        if filename:
            self.process_file_selection(filename)

    def process_file_selection(self, filepath):
        """Hàm trung gian để xử lý file dù là chọn hay kéo thả"""
        self.current_file_path = filepath
        display_name = os.path.basename(filepath)
        
        # Lấy đuôi file và chuyển về chữ thường để so sánh
        _, extension = os.path.splitext(filepath)
        extension = extension.lower()

        self.lbl_instruction.setText(f"File: {display_name}")
        self.lbl_instruction.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 16px;")

        # Logic kiểm tra đuôi file
        if extension == '.txt':
            self.btn_compress.setEnabled(True)      # Bật nén
            self.btn_decompress.setEnabled(False)   # Tắt giải nén
            self.lbl_instruction.setText(f"File: {display_name}\n(Sẵn sàng nén)")
            
        elif extension == '.bin':
            self.btn_compress.setEnabled(False)     # Tắt nén
            self.btn_decompress.setEnabled(True)    # Bật giải nén
            self.lbl_instruction.setText(f"File: {display_name}\n(Sẵn sàng giải nén)")
            
        else:
            # Trường hợp đuôi lạ: Cảnh báo nhẹ hoặc tắt cả hai (tuỳ bạn, ở đây mình tắt cả 2 cho an toàn)
            self.btn_compress.setEnabled(False)
            self.btn_decompress.setEnabled(False)
            self.lbl_instruction.setText(f"File: {display_name}\n(Định dạng không hỗ trợ)")

    def run_compress(self):
        if not self.current_file_path: return
        try:
            huff = Huffman(self.current_file_path)
            output_path = huff.compress()
            QMessageBox.information(self, "Thành công", f"Đã nén file thành công!\nFile lưu tại:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi nén:\n{str(e)}")

    def run_decompress(self):
        if not self.current_file_path: return
        try:
            huff = Huffman(self.current_file_path)
            output_path = huff.decompress(self.current_file_path)
            QMessageBox.information(self, "Thành công", f"Đã giải nén file thành công!\nFile lưu tại:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi giải nén:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = HuffmanApp()
    window.show()
    sys.exit(app.exec())