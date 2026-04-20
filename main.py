# main.py
# Punto de entrada de la aplicacion

import tkinter as tk
from ventana_principal import VentanaPrincipal

def main():
    raiz = tk.Tk()
    app = VentanaPrincipal(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()