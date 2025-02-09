from escpos import printer, capabilities
from datetime import datetime


class Printer:
    # Size constants
    NORMAL_SIZE = 0x00
    DOUBLE_WIDTH = 0x10
    DOUBLE_HEIGHT = 0x01
    DOUBLE_WIDTH_HEIGHT = 0x11
    TRIPLE_WIDTH = 0x20
    QUADRUPLE_WIDTH = 0x30

    # Alignment constants
    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2

    def __init__(self, devfile, baudrate=19200, debug=False) -> None:
        if not debug:
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
        else:
            self.ser = printer.Dummy()
        self.empty_buffer()

    def set_styles(self):
        # self.set_double_strike()
        self.set_print_density(7, 255, 2)
        self.set_margins(0, 0)
        self.set_size(Printer.NORMAL_SIZE)
        self.set_code_page(0)

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

    def set_code_page(self, page=0):
        """
        Change the code page - different character sets. From the manual:
        0: CP437 [U.S.A., Standard Europe]
        1: Katakana
        2: CP850 [Multilingual]
        3: CP860 [Portuguese]
        4: CP863 [Canadian-French]
        5: CP865 [Nordic]
        6: WCP1251 [Cyrillic]
        7: CP866 Cyrilliec #2
        8: MIK[Cyrillic /Bulgarian]
        9: CP755 [East Europe, Latvian 2]
        16: WCP1252 Latin I
        17: WCP1253 [Greek]
        18: CP852 [Latina 2]
        19: CP858 Multilingual Latin I+Euro)
        255: Space page
        """
        self.ser._raw(bytes([0x1B, 0x74, page]))

    # Text Formatting Methods
    def set_emphasized(self, on=True):
        """
        ESC E n command - Turn emphasized mode on/off
        uses font emphasis
        Does not seem to work well on this model
        """
        self.ser._raw(bytes([0x1B, 0x45, 0x01 if on else 0x00]))

    def set_double_strike(self, on=True):
        """
        ESC G n command - Turn double strike mode on/off
        print each dot twice
        Does not seem to work well on this model
        """
        self.ser._raw(bytes([0x1B, 0x47, 0x01 if on else 0x00]))

    def set_underline(self, mode=0):
        """ESC - n command - Turn underline mode on/off (0=off, 1=1-dot, 2=2-dot)"""
        self.ser._raw(bytes([0x1B, 0x2D, mode]))

    def set_alignment(self, align=ALIGN_LEFT):
        """ESC a n command - Set justification"""
        self.ser._raw(bytes([0x1B, 0x61, align]))

    def text(self, text):
        self.ser.text(text)

    def write_datetime(self):
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.ser.text(current_time)

    def write_divider(self, char="-", length=32):
        """Utility method to print a dividing line"""
        self.text(char * length + "\n")

    def qr(self, *args, **kwargs):
        self.ser._raw(b"\x1b\x21\x00")
        self.ser.qr(*args, **kwargs)

    def empty_buffer(self):
        self.ser._raw(b"\x1b\x40")
        self.set_styles()

    def close(self):
        self.ser.close()
