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

def createPDF(cuit,puntoDeVenta,periodo,totalFacturado,datosDeLosComprobantes,ruta):
  data = obtener_datos_por_cuit(cuit)
  nombreArchivo = ruta +"/" + data.get("RAZON SOCIAL") + " - " +periodo +".txt"

  #DATOS PARA EL ENCABEZADO
  #NUMERO DE CLIENTE
  usuarioGomez = data.get("USER")
  #CONTRIBUYENTE
  contribuyente = data.get("RAZON SOCIAL")
  #LEGAJO
  legajo = data.get("LEGAJO")
  if legajo == "-":
    legajo = "SIN LEGAJO"



  print(f"USER: {usuarioGomez}")
  print(f"CUIT: {cuit}")
  print(f"CONTRIBUYENTE: {contribuyente}")
  print(f"LEGAJO: {legajo}")
  print(f"PUNTO DE VENTA: {puntoDeVenta}")
  print(f"PERIODO: {periodo}")

  tablaDeComprobantes = PrettyTable()
  tablaDeComprobantes.field_names = ["Fecha","Tipo","Número Desde","Nro. Doc. Receptor", "Denominación Receptor","Imp. Total"]

  for elemento in datosDeLosComprobantes:
    if elemento["Nro. Doc. Receptor"] == 0.0:
      nroDocReceptor = ""
    else: 
      nroDocReceptor = elemento["Nro. Doc. Receptor"]

    if elemento["Denominación Receptor"] == 0.0:
      denomReceptor = ""
    else: 
      denomReceptor = elemento["Denominación Receptor"][:16]

    tablaDeComprobantes.add_row([elemento["Fecha"], elemento["Tipo"], elemento["Número Desde"], 
                                 nroDocReceptor, 
                                 denomReceptor, 
                                 elemento["Imp. Total"]])

  tablaDeComprobantes.add_row(["","","","","",""])
  tablaDeComprobantes.add_row(["","","","","Importe Total",totalFacturado])


  # Abre el archivo en modo escritura
  with open(nombreArchivo, "w") as archivo:

    # Escribe los datos en el archivo
    archivo.write(f"USER: {usuarioGomez}\n")
    archivo.write(f"CUIT: {cuit}\n")
    archivo.write(f"CONTRIBUYENTE: {contribuyente}\n")
    archivo.write(f"LEGAJO: {legajo}\n")
    archivo.write(f"PUNTO DE VENTA: {puntoDeVenta}\n")
    archivo.write(f"PERIODO: {periodo}\n")

    # Escribe la tabla en el archivo
    archivo.write(str(tablaDeComprobantes))

    print(f"Los datos se han guardado en el archivo: {nombreArchivo}")

  print (tablaDeComprobantes)

#createPDF(data_cuit,puntoDeVenta,periodo,valorTotal,datosComprobante)