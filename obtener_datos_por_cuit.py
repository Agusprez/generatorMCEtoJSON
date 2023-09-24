import json

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