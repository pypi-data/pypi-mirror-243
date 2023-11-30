import serial
from serial.tools import list_ports
import argparse
import threading
import sys
from datetime import datetime
import logging


class GPSLogger(serial.Serial):
    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N', stopbits=1,
                 timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None,
                 dsrdtr=False, inter_byte_timeout=None, exclusive=None, **kwargs):
        serial.Serial.__init__(self, port, baudrate, bytesize, parity, stopbits,
                               timeout, xonxoff, rtscts, write_timeout, dsrdtr,
                               inter_byte_timeout, exclusive)
        self._read_thread = None
        # self._write_thread = None
        logging.basicConfig(level=logging.INFO)  # Set Info level for root logger
        self._init_threads()
        self._info_logger = None
        self._error_logger = None
        self._is_running = False

    def _init_threads(self):
        self._read_thread = threading.Thread(target=self._read_callback)
        # self._write_thread = threading.Thread(target=self._write_callback)

    @staticmethod
    def list_devices() -> tuple:
        ports = list_ports.comports()
        out = tuple({"device": port.device, "id": f"{hex(port.vid)[2:].zfill(4)}:{hex(port.pid)[2:].zfill(4)}", "description": port.description} for port in ports if port.pid is not None)
        return out

    @classmethod
    def search(cls, vid: str, pid: str, **kwargs):
        v = int(vid, 16)
        p = int(pid, 16)
        ports = list_ports.comports()
        for port in ports:
            if port.vid == v and port.pid == p:
                return cls(port=port.device, **kwargs)
        print(f"Could not find device {vid}:{pid}.", file=sys.stderr)

    def start(self):
        if not self.isOpen():
            print("Call open method first!", file=sys.stderr)
            return

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")

        # Reset and set up info logger
        self._info_logger = logging.getLogger("info_logger")
        for handler in self._info_logger.handlers[:]:
            self._info_logger.removeHandler(handler)
        log_filename = f"log_{timestamp}.log"
        info_handler = logging.FileHandler(log_filename)
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        info_handler.setFormatter(info_formatter)
        # console_handler = logging.StreamHandler()
        # console_handler.setFormatter(info_formatter)
        self._info_logger.addHandler(info_handler)
        # self._info_logger.addHandler(console_handler)

        # Reset and set up error logger
        self._error_logger = logging.getLogger("error_logger")
        self._error_logger.propagate = True
        for handler in self._error_logger.handlers[:]:
            self._error_logger.removeHandler(handler)

        error_log_filename = f"error_{timestamp}.log"
        error_handler = logging.FileHandler(error_log_filename)
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        error_handler.setFormatter(error_formatter)
        self._error_logger.addHandler(error_handler)

        self._is_running = True

        # self._write_thread.start()
        self._read_thread.start()

    def stop(self):
        if not self.isOpen():
            if self._error_logger is not None:
                self._error_logger.error("Serial already closed!")
            return
        print("Closing serial.")
        self._is_running = False
        self._read_thread.join()
        self.close()
        # self._write_thread.join()
        self._init_threads()


    def _read_callback(self):
        while self._is_running:
            try:
                line = self.readline()
                if line is None or not len(line):
                    continue
                self._info_logger.info(line.decode().strip())
            except Exception as e:
                self._error_logger.error(str(e))

    # def _write_callback(self):
    #     while self._is_running:
    #         try:
    #             # Check if input is available
    #             ready, _, _ = select.select([sys.stdin], [], [], 0.1)
    #             if ready:
    #                 msg = sys.stdin.readline().strip()  # Read input line
    #                 self.write(msg.encode())
    #             else:
    #                 # No input, can do other things or sleep briefly
    #                 time.sleep(0.1)
    #         except Exception as e:
    #             self._error_logger.error(str(e))


# def get_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(prog="uBlox GPS Logger",
#                                      description="Logs NMEA 0183 messages from a uBlox GPS.")
#     parser.add_argument("-p", "--product", type=str, help="Product ID hex code (e.g. '01a8'")
#     parser.add_argument("-v", "--vendor", type=str, help="Vendor ID hex code (e.g. '1546'")
#     parser.add_argument("-d", "--device", type=str, help="USB Device (e.g. '/dev/ttyUSB0', 'COM1'")
#     return parser.parse_args()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="uBlox GPS Logger",
                                     description="Logs NMEA 0183 messages from a uBlox GPS.")

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-d", "--device", type=str, help="USB Device (e.g. '/dev/ttyUSB0', 'COM1')")

    # Vendor and Product arguments
    parser.add_argument("-v", "--vendor", type=str, help="Vendor ID hex code (e.g. '1546')")
    parser.add_argument("-p", "--product", type=str, help="Product ID hex code (e.g. '01a8')")

    args = parser.parse_args()

    # Check if both vendor and product are provided if either one is used
    if (args.vendor and not args.product) or (args.product and not args.vendor):
        parser.error("The --vendor and --product arguments must be used together")

    return args

