from PIL import Image
from escpos.printer import Dummy


def tempalte(content, printer):
    printer.text("Debut du contenu")
    printer.text("\n")
    printer.text(content)
    printer.text("\n")
    printer.text("Fin du contenu")
    printer.barcode("4006381333931", "EAN13", 64, 2, "", "")
    printer.qr("https://technopolice.fr/", size=8)
    printer.cut()


def run():
    printer = Dummy()
    tempalte("Le contenu !", printer)

    print(printer.output.decode("ascii", errors="replace"))
    print("")


if __name__ == "__main__":
    run()
