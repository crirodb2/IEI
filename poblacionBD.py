import psycopg

conndata = "dbname=iei user=pi password=pi host=88.17.114.199 port=5432"

def AddCentro(nombre: str, tipo: str, direccion: str, codigoPostal: int = None, longitud: float = None, 
    latitud: float = None, telefono: int = None, descripcion: str = None, localidad: str = None):

    if(codigoPostal == "" or latitud == "" or longitud == ""): return
    if(codigoPostal == None or latitud == None or longitud == None): return

    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = """INSERT INTO establecimientosanitario VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) 
            ON CONFLICT (nombre) 
            DO NOTHING"""

            data = (nombre, tipo, direccion, codigoPostal, longitud, latitud, telefono, descripcion, localidad)

            try:
                cur.execute(SQL,data)
                conn.commit()

            except Exception as error:
                raise error

def AddLocalidad(codigo: str, nombre: str, codprov: str):

    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:
            
            SQL = """INSERT INTO localidad VALUES (%s,%s,%s) 
            ON CONFLICT (nombre) 
            DO NOTHING"""

            data = (codigo, nombre, codprov)

            try:
                cur.execute(SQL,data)
                conn.commit()

            except Exception as error:
                print(str(error))

def AddProvincia(codigo: str, nombre: str):

    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = """INSERT INTO provincia VALUES (%s,%s) 
            ON CONFLICT (nombre) 
            DO NOTHING"""

            data = (codigo, nombre)

            try:
                cur.execute(SQL,data)
                conn.commit()

            except Exception as error:
                raise error

def getLocalidad(nombre: str):
    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = "SELECT codigo FROM localidad WHERE nombre=%s"
            
            data = (nombre,)

            try:
                cur.execute(SQL,data)
                conn.commit()

                a = cur.fetchone()

                return a

            except Exception as error:
                raise error

def getProvincia(nombre: str):
    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = "SELECT codigo FROM provincia WHERE nombre=%s"
            
            data = (nombre,)

            try:
                cur.execute(SQL,data)
                conn.commit()

                a = cur.fetchone()

                return a

            except Exception as error:
                raise error