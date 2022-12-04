import psycopg


conndata = "dbname=bluesky user=pi password=pi host=88.17.114.199 port=5432"

def AddCentro(nombre: str, tipo: str, direccion: str, codigoPostal: int = None, longitud: float = None, 
    latitud: float = None, telefono: int = None, descripcion: str = None):

    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = """INSERT INTO estblecimientosanitario VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
            ON CONFLICT (nombre) 
            DO UPDATE SET 
                tipo = excluded.tipo,
                direccion = excluded.direccion,
                codigoPostal = excluded.codigoPostal,
                longitud = excluded.longitud,
                latitud = excluded.latitud,
                telefono = excluded.telefono,
                descripcion = excluded.descripcion"""

            data = (nombre, tipo, direccion, codigoPostal, longitud, latitud, telefono, descripcion)

            try:
                cur.execute(SQL,data)
                conn.commit()

            except Exception as error:
                raise error

def AddLocalidad(codigo: str, nombre: str):

    with psycopg.connect(conndata) as conn:
        with conn.cursor() as cur:

            SQL = """INSERT INTO localidad VALUES (%s,%s) 
            ON CONFLICT (codigo) 
            DO NOTHING"""

            data = (codigo, nombre)

            try:
                cur.execute(SQL,data)
                conn.commit()

            except Exception as error:
                raise error

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