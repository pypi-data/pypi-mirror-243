import tkinter as tk
from tkinter import scrolledtext
from nmea_gps_logging.logger import GPSLogger


class GPSLoggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GPS Logger")

        # Connect / Disconnect Button
        self.toggle_connection_button = tk.Button(master, text="Connect", command=self.toggle_connection)
        self.toggle_connection_button.pack()

        # Record / Stop Record Button
        self.toggle_record_button = tk.Button(master, text="New Log", command=self.trigger_log, state=tk.DISABLED)
        self.toggle_record_button.pack()

        # Text Area for Status Messages
        self.status_text = scrolledtext.ScrolledText(master, state='disabled', height=10)
        self.status_text.pack()

        # GPS Logger instance
        self.gps_logger = None
        self.is_recording = False

    def select_device_dialog(self):
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

    def toggle_connection(self):
        if self.gps_logger is None:
            selected_device = self.select_device_dialog()
            self.gps_logger = GPSLogger(port=selected_device["device"])  # replace with actual port
            self.gps_logger.start()
            self.toggle_connection_button.config(text="Disconnect")
            self.toggle_record_button.config(state=tk.NORMAL)
            self._log_message("Connected to GPS Logger")
            self._log_message("Logging...")
        else:
            self.gps_logger.stop()
            self.gps_logger = None
            self.toggle_connection_button.config(text="Connect")
            self.toggle_record_button.config(state=tk.DISABLED)
            self._log_message("Stopped logging.")
            self._log_message("Disconnected from GPS Logger")

    def trigger_log(self):
        self.gps_logger.stop()
        self._log_message("New log created.")
        self.gps_logger.open()
        self.gps_logger.start()
        self._log_message("Logging...")

    def _log_message(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state='disabled')


def main():
    root = tk.Tk()
    gui = GPSLoggerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
