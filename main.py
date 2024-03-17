import tkinter as tk
from tkinter import messagebox
import subprocess

def reload_interfaces():
    try:
        # Chạy lệnh để lấy danh sách giao diện
        output = subprocess.check_output(["sudo", "./kdd99_feature_extractor-master/build-files/src/kdd99extractor", "-l"])
        # Decode kết quả và tách danh sách giao diện
        interfaces = [line.split()[-1][1:-1] for line in output.decode("utf-8").split("\n") if line.strip() and not line.startswith("0.")]
        # Xóa tất cả các mục hiện có trong dropdown menu
        interface_dropdown['menu'].delete(0, 'end')
        # Thêm các giao diện vào dropdown menu
        for interface in interfaces:
            interface_dropdown['menu'].add_command(label=interface, command=tk._setit(selected_interface, interface))
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error reloading interfaces")


def run_kdd99extractor():
    # Lấy các giá trị từ các ô nhập liệu
    interface_number = selected_interface.get()
    timeout_ms = timeout_ms_entry.get()
    output_file = output_file_entry.get()
    additional_frame_length = additional_frame_length_entry.get()
    ip_reassembly_timeout = ip_reassembly_timeout_entry.get()
    tcp_syn_timeout = tcp_syn_timeout_entry.get()
    # Thực thi lệnh kdd99extractor với các giá trị tùy chọn
    command = f"sudo ./kdd99_feature_extractor-master/build-files/src/kdd99extractor -i {interface_number} -p {timeout_ms} -o {output_file} -a {additional_frame_length} -ft {ip_reassembly_timeout} -tst {tcp_syn_timeout}"
    try:
        subprocess.run(command.split(), check=True)
        messagebox.showinfo("Success", "kdd99extractor completed successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error running kdd99extractor")

# Tạo cửa sổ giao diện người dùng
root = tk.Tk()
root.title("kdd99extractor GUI")

# Thêm các thành phần giao diện người dùng
tk.Label(root, text="Select Interface:").grid(row=0, column=0, sticky="w")
selected_interface = tk.StringVar(root)
interface_dropdown = tk.OptionMenu(root, selected_interface, "")
interface_dropdown.grid(row=0, column=1)

reload_button = tk.Button(root, text="Reload Interfaces", command=reload_interfaces)
reload_button.grid(row=0, column=2)

# Thêm các ô nhập liệu khác và nút chạy tương tự như trước
tk.Label(root, text="Timeout (ms):").grid(row=1, column=0, sticky="w")
timeout_ms_entry = tk.Entry(root)
timeout_ms_entry.grid(row=1, column=1)

tk.Label(root, text="Output File:").grid(row=2, column=0, sticky="w")
output_file_entry = tk.Entry(root)
output_file_entry.grid(row=2, column=1)

tk.Label(root, text="Additional Frame Length (BYTES):").grid(row=3, column=0, sticky="w")
additional_frame_length_entry = tk.Entry(root)
additional_frame_length_entry.grid(row=3, column=1)

tk.Label(root, text="IP Reassembly Timeout (SECONDS):").grid(row=4, column=0, sticky="w")
ip_reassembly_timeout_entry = tk.Entry(root)
ip_reassembly_timeout_entry.grid(row=4, column=1)

tk.Label(root, text="TCP SYN Timeout (SECONDS):").grid(row=5, column=0, sticky="w")
tcp_syn_timeout_entry = tk.Entry(root)
tcp_syn_timeout_entry.grid(row=5, column=1)

run_button = tk.Button(root, text="Run kdd99extractor", command=run_kdd99extractor)
run_button.grid(row=6, column=0, columnspan=2)

# Bắt đầu vòng lặp chờ sự kiện
root.mainloop()
