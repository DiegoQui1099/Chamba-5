import pymysql

# Configuración de las bases de datos
DATABASES = {
    'db1': {
        'host': '10.210.150.44',
        'user': 'daquinones',
        'password': 'Colombia123#',
        'database': 'cobros_new'
    },
    'db2': {
        'host': '10.210.150.44',
        'user': 'daquinones',
        'password': 'Colombia123#',
        'database': 'ani'
    }
}

# Conexiones a las bases de datos
def get_connection(db_key):
    """
    Devuelve una conexión a la base de datos especificada.
    """
    db_config = DATABASES.get(db_key)
    if not db_config:
        raise ValueError(f"No se encontró configuración para la base de datos: {db_key}")
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

# Configuración general
DEBUG = True
PORT = 400
