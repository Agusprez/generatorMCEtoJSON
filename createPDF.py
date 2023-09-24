#VOY A IR TRABAJANDO ACA PARA REALIZAR LA FUNCION PARA CREAR PDFS
from obtener_datos_por_cuit import obtener_datos_por_cuit
from prettytable import PrettyTable

data_cuit = "20121644852"
periodo = "Agosto 2023"
valorTotal = 15000
puntoDeVenta = 2
datosComprobante = [
  {
      "Fecha": "07/08/2023",
      "Tipo": "11 - Factura C",
      "Punto de Venta": 5,
      "Número Desde": 469,
      "Nro. Doc. Receptor": 30667137736,
      "Denominación Receptor": "OSCAR ALFREDO AEGINIO S R L",
      "Imp. Total": 26000
    },
    {
      "Fecha": "10/08/2023",
      "Tipo": "11 - Factura C",
      "Punto de Venta": 5,
      "Número Desde": 470,
      "Nro. Doc. Receptor": 30711012652,
      "Denominación Receptor": "TIRO FEDERAL",
      "Imp. Total": 7560
    },
    {
      "Fecha": "15/08/2023",
      "Tipo": "11 - Factura C",
      "Punto de Venta": 5,
      "Número Desde": 471,
      "Nro. Doc. Receptor": 30711012652,
      "Denominación Receptor": "TIRO FEDERAL",
      "Imp. Total": 14400
    }
]

def crearPDF(cuit,puntoDeVenta,periodo,totalFacturado,datosDeLosComprobantes):
  data = obtener_datos_por_cuit(cuit)
  
  #DATOS PARA EL ENCABEZADO
  #NUMERO DE CLIENTE
  usuarioGomez = data.get("USER")
  #CONTRIBUYENTE
  contribuyente = data.get("RAZON SOCIAL")
  #PUNTO DE VENTA
  

  print(f"USER: {usuarioGomez}")
  print(f"CONTRIBUYENTE: {contribuyente}")
  print(f"PUNTO DE VENTA: {puntoDeVenta}")
  print(f"PERIODO: {periodo}")

  tabla = PrettyTable()
  tabla.field_names = ["Fecha","Tipo","Número Desde","Nro. Doc. Receptor", "Denominación Receptor","Imp. Total"]

  for elemento in datosDeLosComprobantes:
    tabla.add_row([elemento["Fecha"], elemento["Tipo"], elemento["Número Desde"], elemento["Nro. Doc. Receptor"], elemento["Denominación Receptor"], elemento["Imp. Total"]])
  print (tabla)
  print(f"Total facturado: $ {totalFacturado}")


crearPDF(data_cuit,puntoDeVenta,periodo,valorTotal,datosComprobante)