import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
from tkinter import ttk
import pexpect

class KDD99ExtractorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KDD'99-like Feature Extractor GUI")
        self.create_widgets()
        ttk.Style().theme_use('clam')

    def create_widgets(self):
        # Tạo các thành phần giao diện người dùng
        ttk.Label(self, text="Select Interface:").grid(row=0, column=0, sticky="w")
        self.selected_interface = tk.StringVar(self)
        self.interface_dropdown = ttk.OptionMenu(self, self.selected_interface, "")
        self.interface_dropdown.grid(row=0, column=1, sticky="w")

        self.reload_button = ttk.Button(self, text="Reload Interfaces", command=self.reload_interfaces)
        self.reload_button.grid(row=0, column=2, sticky="w")

        self.listen_button = ttk.Button(self, text="Listen", command=self.start_listen)
        self.listen_button.grid(row=0, column=3, sticky="w")
        self.interface_list = 0

        ttk.Label(self, text="Ouput Directory:").grid(row=2, column=0, sticky="w")
        self.output_directory_entry = ttk.Entry(self, state='readonly')
        self.output_directory_entry.grid(row=2, column=1, sticky="w")

        self.output_directory_button = ttk.Button(self, text="Choose folder",
                                                  command=self.choose_output_directory)
        self.output_directory_button.grid(row=2, column=2, sticky="w")

        ttk.Label(self, text="Ouput Filename:").grid(row=3, column=0, sticky="w")
        self.output_file_entry = ttk.Entry(self)
        self.output_file_entry.grid(row=3, column=1, sticky="w")

        self.reload_interfaces()

    def reload_interfaces(self):
        try:
            # Thực hiện lệnh sudo để tải danh sách giao diện mạng
            interface_list = []
            child = pexpect.spawn("sudo ./kdd99_feature_extractor-master/build-files/src/kdd99extractor -l")
            child.expect("password for h066: ")
            child.sendline("1")
            child.expect(pexpect.EOF)
            output_lines = child.before.decode().split("\n")
            for line in output_lines:
                if line.strip() and not line.startswith("0."):
                    interface_list.append(line.split()[-1][1:-1])
            child.close()
            if len(interface_list) >= 2:
                interface_list.insert(0, "All")
                self.selected_interface.set("All")
            elif len(interface_list) == 1:
                self.selected_interface.set(interface_list[0])
            else:
                self.selected_interface.set("")  # Nếu không có interface nào, đặt giá trị rỗng cho ô chọn

                # Xóa tất cả các lựa chọn cũ và thêm các lựa chọn mới
            self.interface_dropdown['menu'].delete(0, 'end')
            for interface in interface_list:
                self.interface_dropdown['menu'].add_command(label=interface,
                                                            command=tk._setit(self.selected_interface, interface))
            self.interface_list = interface_list
        except pexpect.exceptions.ExceptionPexpect:
            messagebox.showerror("Error", "Error reloading interfaces")

    def start_listen(self):
        interface_val = self.selected_interface.get()  # Lấy số của giao diện được chọn
        interface_number = 0
        for i,j in enumerate(self.interface_list):
            if interface_val == j:
                interface_number = i

        if interface_number:
            try:
                # Thực hiện lệnh sudo để bắt đầu lắng nghe trên giao diện được chọn
                self.child = child = pexpect.spawn(f"sudo ./kdd99_feature_extractor-master/build-files/src/kdd99extractor -i {interface_number} > output_file.txt")
                child.expect("Password:")
                child.sendline("1")
                self.show_output_window()
                child.expect(pexpect.EOF)
                child.close()
            except pexpect.exceptions.ExceptionPexpect:
                messagebox.showerror("Error", f"Error listening on interface {interface_number}")

    def show_output_window(self):
        output_window = tk.Toplevel(self)
        output_window.title("Output File Content")

        text_area = scrolledtext.ScrolledText(output_window, width=60, height=20)
        text_area.pack(expand=True, fill="both")

        with open("./a.csv", "r") as file:
            output_content = file.read()

        text_area.insert(tk.END, output_content)

    def stop_listen(self):
        if self.child.isalive():
            print("Child process is still running")
            self.child.close()
        else:
            print("Child process has terminated")
        pass

    def choose_output_directory(self):
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory_entry.config(state='normal')
            self.output_directory_entry.delete(0, tk.END)
            self.output_directory_entry.insert(0, output_directory)
            self.output_directory_entry.config(state='readonly')

if __name__ == "__main__":
    app = KDD99ExtractorGUI()
    app.mainloop()
