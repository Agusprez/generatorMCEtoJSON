import json
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import time
from datetime import datetime
import locale

# Variables globales para rastrear el estado del procesamiento
archivos_procesados = 0
archivos_generados = 0
errores = False
tiempo_inicio = 0

# FUNCION PARA VER CUANTOS ARCHIVOS JSON HAY QUE PROCESAR

def procesar_carpeta(carpeta):
    global archivos_procesados, archivos_generados, errores
    archivos_procesados = 0
    archivos_generados = 0
    errores = False
    tiempo_inicio = time.time()

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta_archivo = os.path.join(carpeta, archivo)
            archivos_procesados += 1
            try:
                cargar_json(ruta_archivo)
                archivos_generados += 1
            except Exception as e:
                print(f"Error al procesar {ruta_archivo}: {e}")
                errores = True

    mostrar_resumen()

# FUNCION PARA CARGAR EL JSON Y MOSTRAR POR CONSOLA LOS VALORES DESEADOS DEL JSON

from datetime import datetime
import locale

def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as json_file:
            data_dict = json.load(json_file)

        # Establecer la configuración regional a español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

        # Inicializar variables
        totalGeneral = 0
        primerComprobante = None  # Inicialmente no se conoce
        ultimoComprobante = None  # Inicialmente no se conoce
        periodo = None  # Inicialmente no se conoce

        for i, item in enumerate(data_dict):
            for clave in ["Fecha", "Tipo", "Punto de Venta", "Número Desde", "Nro. Doc. Receptor", "Denominación Receptor", "Imp. Total"]:
                if clave in item:
                    if clave == "Fecha":
                        fecha = datetime.strptime(item[clave], "%d/%m/%Y")
                        periodo = fecha.strftime("%B %Y")  # Formato "mes año"
                    print(f"{clave}: {item[clave]}")
                    if clave == "Imp. Total":
                        totalGeneral += item[clave]

            if i == 0:
                primerComprobante = item.get("Número Desde")
            ultimoComprobante = item.get("Número Desde")

            print("--")

        print(f"Datos cargados desde {ruta}")
        print(f"Periodo {periodo}")
        print(f"Comprobantes desde {primerComprobante} hasta {ultimoComprobante}")
        print(f"Total: {totalGeneral}")
    except Exception as e:
        print("Error al cargar el archivo JSON:", e)




def mostrar_resumen():
    global archivos_procesados, archivos_generados, errores, tiempo_inicio
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    tiempo_transcurrido_formateado = time.strftime("%H:%M:%S", time.gmtime(tiempo_transcurrido))

    mensaje = f"Archivos procesados: {archivos_procesados}\nArchivos generados: {archivos_generados}\n"
    mensaje += f"Tiempo empleado: {tiempo_transcurrido_formateado}\n"
    if errores:
        mensaje += "\nHubo errores durante el procesamiento."

    messagebox.showinfo("Resumen del Proceso", mensaje)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        procesar_carpeta(carpeta)

# Crear la ventana de la aplicación
ventana = tk.Tk()
ventana.title("Seleccionar Carpeta con Archivos JSON")

ventana.geometry("400x200")
instrucciones = tk.Label(ventana, text="Script para procesar archivos JSON en una carpeta")
instrucciones.pack(pady=10)

# Botón para seleccionar la carpeta
boton_seleccionar = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=20)
boton_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.quit)
boton_cancelar.pack(pady=10)

ventana.mainloop()