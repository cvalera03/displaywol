import tkinter as tk
import socket
import codecs
import csv

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
textomacvar = tk.StringVar()
textonamevar = tk.StringVar()

f = open("macs.csv", "a")

def encender():
    textomac = textomacvar.get()

    if musta.get() == 1:
        wol(b"\xE0\x3F\x49\xA6\x8D\xA0")
    elif brigi.get() == 1:
        print("brigit")
    elif len(texto) > 0:
        textomayus = textomac.upper()
        mac = textomac.replace(":", "")
        macsin = memoryview(mac.encode("utf-8")).tobytes()
        macbyte = codecs.decode(macsin, "hex") 
        wol(macbyte)

def agregar_mac():
    textomac = textomacvar.get()
    textoname = textonamevar.get()
    separador = ","

    with open("macs.csv", "r") as archivo_csv:
        next(archivo_csv)
        datos = []
        for linea in archivo_csv:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            macdato = columnas[0]
            print(macdato)
            namedato = columnas[1]
            print(namedato)
            datos.append({
                "mac" : macdato,
                "name" : namedato
            })

    print(datos)
    nuevos_datos = {
        "mac" : textomac,
        "name" : textoname
    }
    print(nuevos_datos)
    datos.append(nuevos_datos)
    print(datos)
    with open("macs.csv", "w", newline="") as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["mac", "name"])
        escritor_csv.writeheader()
        for fila in datos:
            escritor_csv.writerow(fila)


# Obtener dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
ancho_ventana = 500
alto_ventana = 300
posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (alto_pantalla - alto_ventana) // 2

# Widgets
etiqueta = tk.Label(ventana, text= "Escoge el ordenador a encender")
etiqueta.pack()

framefijos = tk.Frame(ventana)
framefijos.pack()

casilla = tk.Checkbutton(framefijos, text="Mustapha", variable=musta, onvalue=1, offvalue=0)
casilla.grid(row=1, column=0)

casilla2 = tk.Checkbutton(framefijos, text="Brigitte", variable=brigi, onvalue=1, offvalue=0)
casilla2.grid(row=1, column=1)

framemac = tk.Frame(ventana)
framemac.pack()

labelmac = tk.Label(framemac, text="MAC: ")
labelmac.grid(row=0, column=0)

cuadromac = tk.Entry(framemac, textvariable=textomacvar)
cuadromac.grid(row=0, column=1)

labelname = tk.Label(framemac, text="NOMBRE: ")
labelname.grid(row=0, column=2)

cuadroname = tk.Entry(framemac, textvariable=textonamevar)
cuadroname.grid(row=0, column=3)

boton = tk.Button(ventana, text="Encender", command=encender)
boton.pack()

agregar = tk.Button(ventana, text="Agregar", command=agregar_mac)
agregar.pack()

ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
ventana.mainloop()