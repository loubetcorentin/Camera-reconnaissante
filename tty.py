import numpy as np
from datetime import datetime
import serial
from PIL import Image


class Printer:
    def __init__(self, port, baudrate=19200) -> None:
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )

    # Size constants
    NORMAL_SIZE = 0x00
    DOUBLE_WIDTH = 0x10
    DOUBLE_HEIGHT = 0x01
    DOUBLE_WIDTH_HEIGHT = 0x11
    TRIPLE_WIDTH = 0x20
    QUADRUPLE_WIDTH = 0x30

    def set_print_density(self, dots=7, heating_time=80, heating_interval=2):
        """
        dots: Max printing dots (0-7), default high density of 7 (64 dots)
        heating_time: Heating time (3-255), default 80 (800μs)
        heating_interval: Heating interval (0-255), default 2 (20μs)
        """
        self.ser.write(bytes([0x1B, 0x37, dots, heating_time, heating_interval]))

    def set_size(self, size):
        self.ser.write(bytes([0x1D, 0x21, size]))

    def set_margins(self, left_margin=4, blank_chars=4):
        self.ser.write(bytes([0x1D, 0x4C, left_margin, 0x00]))
        self.ser.write(bytes([0x1B, 0x42, blank_chars]))

    def set_code_page(self, page=0):  # 0 is PC437 (default)
        # ESC t command to select character code table
        self.ser.write(bytes([0x1B, 0x74, page]))

    def write(self, text):
        self.ser.write(f"{text}\n".encode("cp437", errors="replace"))

    def print_bitmap(self, height, width, bitmap_data):
        """
        Print a bitmap using DC2 * command
        height: height of bitmap
        width: width of bitmap
        bitmap_data: array of bytes representing bitmap (1 for black, 0 for white)
        """
        self.ser.write(bytes([0x12, 0x2A, height, width]))  # DC2 * r n
        self.ser.write(bitmap_data)

    def print_datetime(self):
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.write(current_time.encode())

    def print_image(self, image_path):
        """
        Print an image file
        image_path: path to image file
        """
        # Open and convert image to black and white
        image = Image.open(image_path).convert("1")  # '1' mode = binary
        width = image.width
        height = image.height

        # Convert to bitmap data
        pixels = np.array(image)
        bitmap = []
        for y in range(0, height, 8):
            for x in range(width):
                byte = 0
                for bit in range(min(8, height - y)):
                    if y + bit < height and pixels[y + bit, x]:
                        byte |= 1 << (7 - bit)
                bitmap.append(byte)

        self.print_bitmap(height, width, bytes(bitmap))

    def close(self):
        self.ser.close()


# printer = Printer("/dev/tty.usbmodemflip_Rodiki1")
# printer.set_print_density(7, 255, 2)
#
# printer.print("Test print")
# printer.close()
