import tkinter as tk
import socket
import codecs

def wol(luna_mac_address: bytes) -> None:
    """Send a Wake-on-LAN magic packet to the specified MAC address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    magic = b"\xff" * 6 + luna_mac_address * 16
    s.sendto(magic, ("192.168.1.255", 7))

ventana = tk.Tk()
ventana.title("Wake on Lan")

musta = tk.IntVar()
brigi = tk.IntVar()
textovar = tk.StringVar()

def encender():
    texto = textovar.get()

    if musta.get() == 1:
        wol(b"\xE0\x3F\x49\xA6\x8D\xA0")
    elif brigi.get() == 1:
        print("brigit")
    elif len(texto) > 0:
        mac = texto.replace(":", "")
        macsin = memoryview(mac.encode("utf-8")).tobytes()
        macbyte = codecs.decode(macsin, "hex") 
        wol(macbyte)


# Obtener dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
ancho_ventana = 300
alto_ventana = 200
posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (alto_pantalla - alto_ventana) // 2

# Widgets
etiqueta = tk.Label(ventana, text= "Escoge el ordenador a encender")
etiqueta.pack()

casilla = tk.Checkbutton(ventana, text="Mustapha", variable=musta, onvalue=1, offvalue=0)
casilla.pack()

casilla2 = tk.Checkbutton(ventana, text="Brigitte", variable=brigi, onvalue=1, offvalue=0)
casilla2.pack()

boton = tk.Button(ventana, text="Encender", command=encender)
boton.pack()

cuadrotext = tk.Entry(ventana, textvariable=textovar)
cuadrotext.pack()


ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
ventana.mainloop()