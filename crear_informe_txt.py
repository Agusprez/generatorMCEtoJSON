from obtener_datos_por_cuit import obtener_datos_por_cuit

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