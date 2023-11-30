import datetime
import tkinter as tk
from tkinter import scrolledtext, filedialog
from nmea_gps_logging.logger import GPSLogger
from pathlib import Path
from datetime import datetime


class GPSLoggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GPS Logger")

        # Connect / Disconnect Button
        self.toggle_connection_button = tk.Button(master, text="Connect", command=self._toggle_connection)
        self.toggle_connection_button.pack()

        # Record / Stop Record Button
        self.trigger_log_button = tk.Button(master, text="New Log", command=self._trigger_log, state=tk.DISABLED)
        self.trigger_log_button.pack()

        self.toggle_log_button = tk.Button(master, text="Start Logging", command=self._toggle_log, state=tk.DISABLED)
        self.toggle_log_button.pack()

        # Text Area for Status Messages
        self.status_text = scrolledtext.ScrolledText(master, state='disabled', height=10)
        self.status_text.pack(fill="both", expand=True)

        # Button for selecting save directory
        self.select_dir_button = tk.Button(master, text="Select Directory", command=self._select_directory)
        self.select_dir_button.pack()

        self.save_directory = str(Path(".").resolve())

        # GPS Logger instance
        self.gps_logger = None
        self._is_logging = False

        self._log_message(f"Current log directory: {self.save_directory}")

    def _toggle_log(self):
        if not self._is_logging:
            self._start_logging()
        else:
            self._stop_logging()

    def _start_logging(self):
        self.toggle_log_button.config(text="Stop Logging")
        self.gps_logger.start_logging()
        self._is_logging = True
        self.trigger_log_button.config(state=tk.NORMAL)
        self._log_message("Logging started.")

    def _stop_logging(self):
        self.toggle_log_button.config(text="Start Logging")
        self.gps_logger.stop_logging()
        self._is_logging = False
        self.trigger_log_button.config(state=tk.DISABLED)
        self._log_message("Logging stopped.")

    def _select_directory(self):
        # Open the directory selection dialog
        selected_directory = filedialog.askdirectory()
        if selected_directory:  # If a directory was selected
            self.save_directory = selected_directory
            # You can also update a status label or text area to show the selected directory
            self._log_message(f"Selected directory: {self.save_directory}")

    def _select_device_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Select Device")

        listbox = tk.Listbox(dialog)
        listbox.pack(padx=10, pady=10, fill="both", expand=True)

        devices = GPSLogger.list_devices()
        for device in devices:
            listbox.insert(tk.END, f"{device['description']} ({device['id']})")

        # Variable to store the selected device
        selected_device = [None]

        def on_ok():
            selected_index = listbox.curselection()
            if selected_index:
                selected_device[0] = devices[selected_index[0]]
            dialog.destroy()

        ok_button = tk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=5)

        dialog.transient(self.master)  # Set to be on top of the main window
        dialog.grab_set()  # Prevent interaction with main window until this one is closed
        self.master.wait_window(dialog)  # Wait for the dialog to be closed

        return selected_device[0]

    def _toggle_connection(self):
        if self.gps_logger is None:
            selected_device = self._select_device_dialog()
            if selected_device is None:
                return
            self.gps_logger = GPSLogger(port=selected_device["device"])  # replace with actual port
            self.gps_logger.set_log_dir(self.save_directory)
            self.gps_logger.start()
            self.toggle_connection_button.config(text="Disconnect")
            self.toggle_log_button.config(state=tk.NORMAL, text="Start Logging")
            self._log_message(f"Connected to GPS: {selected_device['description']}")
            self.select_dir_button.config(state=tk.DISABLED)
        else:
            self.gps_logger.stop()
            if self._is_logging:
                self._stop_logging()
            self.gps_logger = None
            self.toggle_connection_button.config(text="Connect")
            self.toggle_log_button.config(state=tk.DISABLED, text="Start Logging")
            self._log_message("Disconnected from GPS Logger")
            self.select_dir_button.config(state=tk.NORMAL)

    def _trigger_log(self):
        self.gps_logger.stop_logging()
        self._log_message("New log created.")
        self.gps_logger.start_logging()
        self._log_message("Logging...")

    def _log_message(self, message):
        self.status_text.config(state='normal')
        ts = datetime.utcnow().isoformat()
        self.status_text.insert(tk.END, f"[{ts}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')


def main():
    root = tk.Tk()
    gui = GPSLoggerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
