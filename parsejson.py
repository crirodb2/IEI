import json
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import poblacionBD as p
import os

#os.environ['MOZ_HEADLESS'] = '1'

def CargarEUS():
    with open('EUS.json', 'r') as f:
        data = json.load(f)
    
    for element in data:
        element["Tipodecentro"] = CambiarTipoEUS(element["Tipodecentro"])

    for element in data:
        p.AddCentro(
            element["Nombre"],
            element["tipo"],
            element["Direccion"],
            element["Codigopostal"],
            element["LONWGS84"],
            element["LATWGS84"],
            element["Telefono"],
            element["HorarioatencionCiudadana"]
        )

        p.AddLocalidad(

        )

        p.AddProvincia(

        )

    with open ("./eusmodificado.json", "w") as res:
        json.dump(data, res, indent = 2)
        
def CambiarTipoEUS(centro: str):
    if(centro == "Hospital"): return "Hospital"
    elif(centro == "Centro de Salud" or centro == "Consultorio" or centro == "Ambulatorio" or centro == "Centro de Salud Mental"): return "Centro de Salud"
    else: return "Otros"


def CargarGVA():
    with open('comunidadValenciana.json', 'r') as f:
        data = json.load(f)
    
    for element in data:
        element["Tipus_centre / Tipo_centro"] = CambiarTipoGVA(element["Tipus_centre / Tipo_centro"])

    for element in data:
        p.AddCentro(
            element["Centre / Centro"],
            element["Tipus_centre / Tipo_centro"],
            element["Adreça / Dirección"],
            #CodigoPostal
            #Longitud
            #Latitud
            #Telefono
            element["Dependència_funcional / Dependencia_funcional"]
        )
        
        p.AddLocalidad(

        )

        p.AddProvincia(

        )

    with open ("./gvamodificado.json", "w") as res:
        json.dump(data, res, indent = 2)

def CambiarTipoGVA(centro: str):
    if(centro == "HOSPITALES DE MEDIA Y LARGA ESTANCIA" 
        or centro == "HOSPITALES DE SALUD MENTAL Y TRATAMIENTO DE TOXICOMANÍAS"
        or centro == "HOSPITALES ESPECIALIZADOS" 
        or centro == "HOSPITALES GENERALES"): return "Hospital"
    elif(centro == "CENTRO/SERVICIO DE URGENCIAS Y EMERGENCIAS" 
        or centro == "CENTROS DE CIRUGIA MAYOR AMBULATORIA" 
        or centro == "CENTROS DE ESPECIALIDADES" 
        or centro == "CENTROS DE SALUD"
        or centro == "CENTROS DE SALUD MENTAL"
        or centro == "CENTROS POLIVALENTES"
        or centro == "CONSULTORIOS DE ATENCIÓN PRIMARIA"): return "Centro de Salud"
    else: return "Otros"

def CargarIB():
    with open('Baleares.json', 'r') as f:
        data = json.load(f)
    
    for element in data:
        element["funcio"] = CambiarTipoIB(element["funcio"])
        
    for element in data:
        p.AddCentro(
            element["nom"],
            element["funcio"],
            element["adreca"],
            #CodigoPostal
            element["long"],
            element["lat"],
            #Telefono
            None
        )

        p.AddLocalidad(
            #Codigo
            element["municipi"]
        )

        p.AddProvincia(
            "07",
            "Illes Balears"
        )

    with open ("./ibmodificado.json", "w") as res:
        json.dump(data, res, indent = 2)

def CambiarTipoIB(centro: str):
    if(centro == "UNITAT BASICA" or centro == "CENTRE SANITARI"): return "Centro de Salud"
    elif(centro == "CENTRE SANITARI PREVIST"): return "Otros"
    else: return "Hospital"


def funcionSelenium():
    driver = webdriver.Firefox()
    driver.get("https://www.latlong.net")

    elem = driver.find_element(By.ID, "place")

    elem.send_keys("CALLE EMPARRADO  3")

    l = driver.find_element(By.XPATH,"//html/body/main/div[2]/div[1]/form/button")

    driver.execute_script("arguments[0].click();", l)

    lat = driver.find_element(By.ID, "lat")
    lon = driver.find_element(By.ID, "lng")

    print(lat)
    print(lon)

funcionSelenium()

#CargarEUS()
#CargarGVA()
#CargarIB()