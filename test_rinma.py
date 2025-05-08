import subprocess
from pathlib import Path

def main():
    # print("coucou mageuuuuuuuuuuuule")
    try:
        print("couuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuule ta life")

        basepath = Path("C:/Users/coren/Documents/these/Camera-reconnaissante")
        python = basepath / ".venv" / "Scripts" / "python.exe"
        llava = basepath / "llava.py"

        # print("python :", python)
        # print("llava :", llava)

        subprocess.Popen([str(python), str(llava)], shell=False)
        # print("iciiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")	

    except Exception as e:
        print("Erreur :", e)

# Appel direct si le script est exécuté
if __name__ == "__main__":
    main()
