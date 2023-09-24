from obtener_datos_por_cuit import obtener_datos_por_cuit
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("pdfPLANTILLA"))
template = env.get_template("template.html")

usuario = {
    "CUIT" : "2039111747",
    "razonSocial" : "PEREZ AGUSTIN GABRIEL",
    "PERIODO" : "AGOSTO 2023",
    "PUNTO DE VENTA":1,
    "userGomez": 001

}

def crearPDF(cuit,primerComprobante, ultimoComprobante, periodo, valorTotal,datosComprobante):
    

    #print(f"Llame a la funcion crearPDF con el cuit {cuit}")
    #print(f"Comprobantes desde {primerComprobante} hasta {ultimoComprobante}")
    #print(f"Periodo {periodo}")
    #print("--")
    #print("Aca voy a imprimir el JSON que le paso con los datos de los comprobantes")
    #print(f"{datosComprobante}")
    print("--")
    #print(f"Total {valorTotal}")