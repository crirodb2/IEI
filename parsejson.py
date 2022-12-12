import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import poblacionBD as p
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['MOZ_HEADLESS'] = '1'

def CargarEUS():
    with open('EUS.json', encoding="utf8") as f:
        data = json.load(f)
    
    for element in data:
        element["Tipodecentro"] = CambiarTipoEUS(element["Tipodecentro"])

    i=0
    for element in data:
        p.AddProvincia(
            "PEUS"+str(i),
            element["Provincia"]
        )

        p.AddLocalidad(
            "LEUS"+str(i),
            element["Municipio"],
            p.getProvincia(element["Provincia"])[0]
        )

        try:
            p.AddCentro(
                element["Nombre"],
                element["Tipodecentro"],
                element["Direccion"],
                element["Codigopostal"],
                element["LONWGS84"],
                element["LATWGS84"],
                element["Telefono"],
                element["HorarioatencionCiudadana"],
                p.getLocalidad(element["Municipio"])[0]
            )
        except Exception as error: print("ERROR en CargarEUS "+element["Nombre"]+" "+str(error))

        i+=1
        
def CambiarTipoEUS(centro: str):
    if(centro == "Hospital"): return "Hospital"
    elif(centro == "Centro de Salud" or centro == "Consultorio" or centro == "Ambulatorio" or centro == "Centro de Salud Mental"): return "Centro de Salud"
    else: return "Otros"


def CargarGVA():
    with open('GVA.json', encoding="utf8") as f:
        data = json.load(f)
    
    for element in data:
        element["Tipus_centre / Tipo_centro"] = CambiarTipoGVA(element["Tipus_centre / Tipo_centro"])

    for element in data:
        p.AddProvincia(
            element["Codi_província / Código_provincia"],
            element["Província / Provincia"]
        )

        p.AddLocalidad(
            element["Codi_municipi / Código_municipio"],
            element["Municipi / Municipio"],
            p.getProvincia(element["Província / Provincia"])[0]
        )

        cp = None
        lat = None
        lon = None

        try:
            lat,lon=ObtenerLatLon(element["Adreça / Dirección"])
            cp=ObtenerCP(element["Adreça / Dirección"]+" "+element["Província / Provincia"])
        except Exception: 0
        try:
            p.AddCentro(
                element["Centre / Centro"],
                element["Tipus_centre / Tipo_centro"],
                element["Adreça / Dirección"],
                cp,
                lat,
                lon,
                None,
                element["Dependència_funcional / Dependencia_funcional"],
                p.getLocalidad(element["Municipi / Municipio"])[0]
            )
        except Exception as error: print("ERROR en CargarGVA "+element["Centre / Centro"]+" "+str(error))
        

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
    with open('Baleares.json', "r") as f:
        data = json.load(f)
    
    for element in data:
        element["funcio"] = CambiarTipoIB(element["funcio"])
        
    i=0
    for element in data:
        p.AddProvincia(
            "07",
            "Illes Balears"
        )

        p.AddLocalidad(
            "IB"+str(i),
            element["municipi"],
            "07"
        )

        cp = None

        try:
            cp=ObtenerCP(element["adreca"]+" "+element["municipi"])
        except Exception: next
        try:
            p.AddCentro(
                element["nom"],
                element["funcio"],
                element["adreca"],
                cp,
                element["long"],
                element["lat"],
                None,
                "Disponible",
                p.getLocalidad(element["municipi"])[0]
            )
        except Exception: print("ERROR en CargarIB "+element["nom"])

        i+=1

def CambiarTipoIB(centro: str):
    if(centro == "UNITAT BASICA" or centro == "CENTRE SANITARI"): return "Centro de Salud"
    elif(centro == "CENTRE SANITARI PREVIST"): return "Otros"
    else: return "Hospital"

def ObtenerLatLon(direccion: str):
    geoDisabled = webdriver.FirefoxOptions()

    geoDisabled.set_preference("geo.enabled", False)
    driver = webdriver.Firefox(options=geoDisabled)

    driver.implicitly_wait(3)

    driver.get("https://www.map-gps-coordinates.com")

    elem = driver.find_element(By.ID, "address")

    elem.send_keys(direccion)

    l = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div[1]/form/input[2]")
    
    driver.execute_script("arguments[0].click();", l)
    
    l = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/a")
    
    driver.execute_script("arguments[0].click();", l)

    lat = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[1]').text
    lon = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div[2]/div[2]/div/div[4]/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[2]').text

    driver.quit()

    return lat,lon


def ObtenerCP(direccion: str):
    geoDisabled = webdriver.FirefoxOptions()

    geoDisabled.set_preference("geo.enabled", False)
    driver = webdriver.Firefox(options=geoDisabled)
    driver.implicitly_wait(2)

    driver.get("https://worldpostalcode.com/")

    elem = driver.find_element(By.ID, 'search')

    elem.send_keys(direccion)

    l = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/form/input[1]")
    
    driver.execute_script("arguments[0].click();", l)

    l = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/form/input[1]")
    
    driver.execute_script("arguments[0].click();", l)
    driver.execute_script("arguments[0].click();", l)

    elem = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="map_canvas"]/div[1]/div[6]/div/div[1]/div/div[1]/b')))

    cp = driver.find_element(By.XPATH, '//*[@id="map_canvas"]/div[1]/div[6]/div/div[1]/div/div[1]/b').text

    driver.quit()

    return cp

#CargarEUS()
CargarGVA()
CargarIB()