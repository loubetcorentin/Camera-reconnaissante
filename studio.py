import os
import time
from pathlib import Path
from tty import Printer

from dotenv import load_dotenv

load_dotenv()

SERIAL_PATH = str(os.getenv("SERIAL_PATH"))
OUTPUT_MSG_FILE = Path(str(os.getenv("OUTPUT_MSG_FILE")))


def run():
    printer = Printer(SERIAL_PATH, debug=False)
    printer.ser.image("./img/ami.jpg", center=True)
    with open(OUTPUT_MSG_FILE, "r") as file:
        content = file.read()
        for i, chunck in enumerate(content.split("\n\n")):
            printer.ser.ln()
            printer.write_divider()
            printer.ser.ln()
            match i:
                case 0:
                    printer.set_emphasized(True)
                    printer.text(chunck)
                    printer.set_emphasized(False)
                case 1:
                    printer.set_underline(True)
                    printer.text(chunck)
                    printer.set_underline(False)
                case _:
                    printer.text(chunck)
            time.sleep(5)
    printer.ser.ln()
    time.sleep(5)
    printer.ser.barcode("4006381333931", "EAN13", 64, 2, "", "")
    printer.qr("https://technopolice.fr/", size=2)

    # print(printer.ser.output.decode("ascii", errors="replace"))
    print("")


if __name__ == "__main__":
    run()
