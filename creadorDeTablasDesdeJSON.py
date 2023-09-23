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


def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        data_cuit = json_data.get("CUIT")
        data_dict = json_data.get("datosFacturacion", [])
        # Establecer la configuración regional a español
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

        # Inicializar variables
       
        primerComprobante = None  # Inicialmente no se conoce
        ultimoComprobante = None  # Inicialmente no se conoce
        periodo = None  # Inicialmente no se conoce
        puntoDeVenta = None
        #Aca tengo que definir lso acumuladores, de ventas y de notas de credito
        totalPositivo = 0
        totalNegativo = 0
        #Tengo que crear un arreglo para ir guardando los datos de los comprobantes para luego mandarlo a crearPDF
        
        
        datosComprobante = []

        for i, item in enumerate(data_dict):
            datos_comprobante_actual = {}
            #Esta iteracion hace referencia cada uno de los datos dentro de Datos Facturacion del JSON
            for clave in ["Fecha", "Tipo", "Punto de Venta", "Número Desde", "Nro. Doc. Receptor", "Denominación Receptor", "Imp. Total"]:
                if clave in item:
                    if clave == "Fecha":
                        fecha = datetime.strptime(item[clave], "%d/%m/%Y")
                        periodo = fecha.strftime("%B %Y")  # Formato "mes año"
                    datos_comprobante_actual[clave] = item[clave]
                    if clave == "Tipo":
                        if item[clave] == "13 - Nota de Crédito C":
                            totalNegativo += item.get("Imp. Total", 0)
                            #datosComprobante.append({"clave": clave, "valor": item[clave]})
                        elif item[clave] == "9 - Recibo C":
                            totalPositivo = totalPositivo    
                        else: 
                            totalPositivo += item.get("Imp. Total", 0)   
                            #datosComprobante.append({"clave": clave, "valor": item[clave]}) 



            datosComprobante.append(datos_comprobante_actual)
            if i == 0:
                primerComprobante = item.get("Número Desde")
            if item["Tipo"] == "11 - Factura C":
                ultimoComprobante = item.get("Número Desde")
        print("----")
        puntoDeVenta = (datosComprobante[0].get("Punto de Venta"))
        valorTotal = totalPositivo - totalNegativo
        #crearPDF(data_cuit, primerComprobante, ultimoComprobante, periodo, valorTotal,datosComprobante)
        crear_informe_txt(data_cuit,primerComprobante,ultimoComprobante,periodo,valorTotal,puntoDeVenta)
        print("----")
    except Exception as e:
        print("Error al cargar el archivo JSON:", e)

def crear_informe_txt(cuit, primerComprobante, ultimoComprobante, periodo, valorTotal,puntoDeVenta):
    # Abrir el archivo en modo escritura (se creará o sobrescribirá si ya existe)

    nombreArchivo = "C:/Users/perez/OneDrive/Documentos/data MCE/reporteDeVentas - " + periodo + ".txt"
    with open(nombreArchivo, "a", encoding="utf-8") as archivo_txt:
        datosJSON = obtener_datos_por_cuit(cuit)
        razonSocial = datosJSON.get("RAZON SOCIAL")
        userGomez = datosJSON.get("USER")

        if userGomez == "-":
            userGomez = "Sin usuario definido"

        archivo_txt.write("------------------------------\n")
        archivo_txt.write(f"USER {userGomez}\n")
        archivo_txt.write(f"CUIT {cuit}\n")
        archivo_txt.write(f"Razon Social {razonSocial}\n")
        archivo_txt.write(f"Punto de Venta: {puntoDeVenta}\n")
        archivo_txt.write(f"Comprobantes desde {primerComprobante} hasta {ultimoComprobante}\n")
        archivo_txt.write(f"Periodo: {periodo}\n")        
        archivo_txt.write(f"Total: {valorTotal}\n")
        archivo_txt.write("------------------------------\n")

def crearPDF(cuit,primerComprobante, ultimoComprobante, periodo, valorTotal,datosComprobante):
    print(f"Llame a la funcion crearPDF con el cuit {cuit}")
    print(f"Comprobantes desde {primerComprobante} hasta {ultimoComprobante}")   
    print(f"Periodo {periodo}")
    print("--")
    print("Aca voy a imprimir el JSON que le paso con los datos de los comprobantes")
    print(f"{datosComprobante}")
    print("--")
    print(f"Total {valorTotal}")

#Funcion para leer los datos que tengo cargado en un JSON, para poder tener Razon Social, y otros datos
def obtener_datos_por_cuit(cuit):
    try:
        with open('C:/Users/perez/OneDrive/Documentos/Generador Estudio/BBDD.json', 'r') as archivo:
            datos = json.load(archivo)
            for entrada in datos:
                if entrada.get("CUIT") == cuit:
                    return entrada
            return {"error": "CUIT no encontrado"}
    except FileNotFoundError:
        return {"error": "Archivo JSON no encontrado"}
    except Exception as e:
        return {"error": str(e)}


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