import tkinter as tk
from tkinter import filedialog


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KDD'99-like Feature Extractor GUI")
        self.create_widgets()

    def create_widgets(self):
        # Create menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)

        list_menu = tk.Menu(menu)
        menu.add_cascade(label="List Interfaces", menu=list_menu)

        run_menu = tk.Menu(menu)
        menu.add_cascade(label="Run", menu=run_menu)

        # Create labels and entry fields
        labels = ["Interface Number:", "Read Timeout (ms):", "Extra Features:", "Print Filename:", "Output File:",
                  "Additional Frame Length (Bytes):", "IP Reassembly Timeout (Seconds):",
                  "Timed Out IP Fragments Lookup (ms):",
                  "TCP SYN Timeout (S0, S1) (Seconds):", "TCP Established Timeout (Seconds):",
                  "TCP RST Timeout (REJ, RSTO, etc.) (Seconds):",
                  "TCP FIN Timeout (S2, S3) (Seconds):", "TCP Last ACK Timeout (Seconds):", "UDP Timeout (Seconds):",
                  "ICMP Timeout (Seconds):", "Timed Out Connection Lookup (ms):", "Time Window Size (ms):",
                  "Count Window Size:"]

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i)
            tk.Entry(self.root).grid(row=i, column=1)

        tk.Checkbutton(self.root, text="IPs, Ports, End Timestamp").grid(row=2, column=1)
        tk.Checkbutton(self.root, text="Before Parsing Each File").grid(row=3, column=1)
        tk.Button(self.root, text="Choose File...", command=self.choose_file).grid(row=4, column=1)

    def choose_file(self):
        filename = filedialog.askopenfilename()
        return filename


root = tk.Tk()
app = GUI(root)
root.mainloop()
