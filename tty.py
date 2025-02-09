from escpos import printer, capabilities
from datetime import datetime


class Printer:
    def __init__(self, devfile, baudrate=19200, debug=False) -> None:
        self.ser = printer.Serial(
            devfile=devfile,
            baudrate=baudrate,
            bytesize=8,
            parity="N",
            stopbits=1,
            rtscts=False,  # Add hardware flow control setting
            dsrdtr=False,  # Add hardware flow control setting
            # profile="ZJ-5870",
        )
        self.init()

    def init(self):
        self.set_print_density(7, 255, 2)
        self.set_margins(0, 0)
        self.set_size(Printer.NORMAL_SIZE)
        self.set_code_page(0)

    # Size constants
    NORMAL_SIZE = 0x00
    DOUBLE_WIDTH = 0x10
    DOUBLE_HEIGHT = 0x01
    DOUBLE_WIDTH_HEIGHT = 0x11
    TRIPLE_WIDTH = 0x20
    QUADRUPLE_WIDTH = 0x30

    def set_size(self, size):
        self.ser._raw(bytes([0x1D, 0x21, size]))

    def set_print_density(self, dots=7, heating_time=80, heating_interval=2):
        """
        dots: Max printing dots (0-7), default high density of 7 (64 dots)
        heating_time: Heating time (3-255), default 80 (800μs)
        heating_interval: Heating interval (0-255), default 2 (20μs)
        """
        self.ser._raw(bytes([0x1B, 0x37, dots, heating_time, heating_interval]))

    def set_margins(self, left_margin=4, blank_chars=4):
        self.ser._raw(bytes([0x1D, 0x4C, left_margin, 0x00]))
        self.ser._raw(bytes([0x1B, 0x42, blank_chars]))

    def set_code_page(self, page=0):  # 0 is PC437 (default)
        self.ser._raw(bytes([0x1B, 0x74, page]))

    def text(self, text):
        self.ser.text(text)

    def write_datetime(self):
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.ser.text(current_time)

    def qr(self, *args, **kwargs):
        self.ser._raw(b"\x1b\x21\x00")
        self.ser.qr(*args, **kwargs)

    def empty_buffer(self):
        self.ser._raw(b"\x1b\x40")
        self.init()

    def close(self):
        self.ser.close()
