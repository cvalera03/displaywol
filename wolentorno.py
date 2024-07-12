import tkinter as tk
import socket
import codecs
import csv
import os.path as path
from tkinter import messagebox as Messagebox

ventana = tk.Tk()
ventana.title("Wake on Lan")

#Variables
macvar = tk.StringVar()
textonamevar = tk.StringVar()
ifnotexist = [{"mac" : "mac", "name" : "name"}]
nomcsv = "macs.csv"
broadcast = "192.168.1.255" #IFCONFIG(LINUX) IPCONFIG(WINDOWS)

#WOL
def wol(luna_mac_address: bytes) -> None:
    """Send a Wake-on-LAN magic packet to the specified MAC address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    magic = b"\xff" * 6 + luna_mac_address * 16
    s.sendto(magic, (broadcast, 7))

#Crea el archivo csv si no existe
if not path.exists(nomcsv):
    f = open(nomcsv, "a")
    with open(nomcsv, "w", newline="") as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["mac", "name"])
        escritor_csv.writeheader()
        
def leer_datos():
    global datos
    separador = ","
    with open(nomcsv, "r") as archivo_csv:
        next(archivo_csv)
        datos = []
        for linea in archivo_csv:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            macdato = columnas[0]
            namedato = columnas[1]
            datos.append({
                "mac" : macdato,
                "name" : namedato
            })

def limpselec(seleccion):
    global selec
    selestr1 = str(seleccion)
    selestr2 = selestr1.replace("(", "")
    selestr3 = selestr2.replace(")", "")
    selestr = selestr3.replace(",", "")
    selec = int(selestr)

def leercsv():
    with open(nomcsv, "w", newline="") as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["mac", "name"])
        escritor_csv.writeheader()
        for fila in datos:
            escritor_csv.writerow(fila)

def fixmac(macUser):
    global mac
    mac = macUser.replace(":", "").replace("-", "")
    mac = memoryview(mac.encode("utf-8")).tobytes()
    mac = codecs.decode(mac, "hex")

#Enciende con WOL E0:3F:49:A6:8D:A0 b"\xE0\x3F\x49\xA6\x8D\xA0" MUSTA
def encender():
    macv = macvar.get()
    seleccion = listamac.curselection()

    if len(macv) > 0:
        fixmac(macUser=macv)
        wol(mac)
    elif seleccion:   
        leer_datos()
        limpselec(seleccion=seleccion)
        
        dicget = datos[selec]
        dicmacint = dicget.get("mac")
        dicmac = str(dicmacint)

        fixmac(macUser=dicmac)
        wol(mac)
    
#Agrega a la lista la informacion
def agregar_mac():
    textomac = macvar.get()
    textoname = textonamevar.get()
    
    leer_datos()

    nuevos_datos = {
        "mac" : textomac,
        "name" : textoname
    }

    datos.append(nuevos_datos)

    leercsv()
    
    cuadromac.delete(0, tk.END)
    cuadroname.delete(0, tk.END)
    actualizar_csv()

#Actualiza la informacion para mostrarla en pantalla
def actualizar_csv():
    separador = ","
    listamac.delete(0, tk.END)
    with open(nomcsv, "r") as archivo_csv:
        next(archivo_csv)
        for linea in archivo_csv:
            linea = linea.rstrip("\n")
            columnas = linea.split(separador)
            macleer = columnas[0]
            nameleer = columnas[1]
            elementos = [f"MAC: {macleer}, Nombre: {nameleer}"]
            for elemento in elementos:
                listamac.insert(tk.END, elemento)

def borrar():
    seleccion = listamac.curselection()
    if not seleccion:
        Messagebox.showinfo("Error!", "Deberias selecionar una MAC.")
        return

    listamac.delete(seleccion)
    leer_datos()
    limpselec(seleccion=seleccion)
    datos.pop(selec)
    leercsv()

# Obtener dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
ancho_ventana = 375
alto_ventana = 250
posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (alto_pantalla - alto_ventana) // 2

# Widgets
etiqueta = tk.Label(ventana, text= "Escoge el ordenador a encender: ")
etiqueta.pack()

framefijos = tk.Frame(ventana)
framefijos.pack()

framemac = tk.Frame(ventana)
framemac.pack()

labelmac = tk.Label(framemac, text="MAC: ")
labelmac.grid(row=0, column=0)

cuadromac = tk.Entry(framemac, textvariable=macvar)
cuadromac.grid(row=0, column=1)

labelname = tk.Label(framemac, text="NOMBRE: ")
labelname.grid(row=0, column=2)

cuadroname = tk.Entry(framemac, textvariable=textonamevar)
cuadroname.grid(row=0, column=3)

botones = tk.Frame(ventana)
botones.pack()

boton = tk.Button(botones, text="Encender", command=encender)
boton.grid(row=0, column=0)

agregar = tk.Button(botones, text="Agregar", command=agregar_mac)
agregar.grid(row=0, column=1)

eliminar = tk.Button(botones, text="Eliminar", command=borrar)
eliminar.grid(row=0, column=2)

scrollbar = tk.Scrollbar(ventana, orient=tk.VERTICAL)
listamac = tk.Listbox(ventana, width=50, height=10, yscrollcommand=scrollbar.set, selectmode="extended")
scrollbar.config(command=listamac.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listamac.pack()

#Funciones nada mas iniciar
actualizar_csv()

#Crea la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
ventana.mainloop()