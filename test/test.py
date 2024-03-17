import tkinter as tk
from tkinter import filedialog
import subprocess


def select_file():
    file_path = filedialog.askopenfilename()
    analyze_log(file_path)


def analyze_current_snort_log():
    snort_log_path = "/var/log/snort/alert.log"  # Đường dẫn đến tệp log của Snort, hãy thay đổi tùy theo hệ thống của bạn
    analyze_log(snort_log_path)


def analyze_log(file_path):
    if not file_path:
        return

    print("Dữ liệu log đã được phân tích và hiển thị.")


# Tạo giao diện
root = tk.Tk()
root.title("Phân tích Log")

# Tạo nút để chọn file log
select_file_button = tk.Button(root, text="Chọn File Log", command=select_file)
select_file_button.pack()

# Tạo nút để phân tích log của Snort đang chạy hiện tại
analyze_current_log_button = tk.Button(root, text="Phân tích Log Snort Hiện Tại", command=analyze_current_snort_log)
analyze_current_log_button.pack()

# Chạy ứng dụng
root.mainloop()
