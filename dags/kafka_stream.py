# Importaciones necesarias para el script
import uuid  # Utilizado para generar identificadores únicos
from datetime import datetime  # Para trabajar con fechas y horas
from airflow import DAG  # Importa la clase DAG de Airflow para definir flujos de trabajo
from airflow.operators.python import PythonOperator  # Permite ejecutar funciones Python como tareas en Airflow
import requests  # Para realizar solicitudes HTTP a APIs externas
import json  # Para trabajar con datos en formato JSON
from kafka import KafkaProducer  # Para enviar mensajes a un tema en Kafka
import time  # Para trabajar con funciones relacionadas con el tiempo
import logging  # Para registrar mensajes de error o información

# Argumentos predeterminados para el DAG de Airflow
default_args = {
    'owner': 'airscholar',  # Propietario del DAG, típicamente el creador o el responsable del mantenimiento
    'start_date': datetime(2023, 9, 3, 10, 00)  # Fecha de inicio del DAG, no ejecuta tareas antes de esta fecha
}

# Función para obtener datos de una API externa
def get_data():
    # Realiza una solicitud GET a la API de usuarios aleatorios y convierte la respuesta a JSON
    res = requests.get("https://randomuser.me/api/")
    res = res.json()  # Parsea la respuesta a formato JSON
    res = res['results'][0]  # Selecciona el primer usuario de los resultados
    return res  # Devuelve los datos del usuario

# Función para formatear los datos obtenidos de la API
def format_data(res):
    data = {}  # Diccionario para almacenar los datos formateados
    location = res['location']  # Extrae la ubicación del usuario
    # Asigna los valores extraídos y formateados al diccionario 'data'
    data['id'] = str(uuid.uuid4())  # Genera un ID único y lo convierte a cadena
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data  # Devuelve los datos formateados

# Función principal que gestiona la obtención, formateo y envío de datos a Kafka
def stream_data():
    # Crea un productor de Kafka configurado para conectarse a un broker en 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    curr_time = time.time()  # Obtiene el tiempo actual

    while True:
        if time.time() > curr_time + 60:  # Ejecuta el bucle durante 1 minuto
            break
        try:
            res = get_data()  # Obtiene datos de la API
            res = format_data(res)  # Formatea los datos obtenidos
            # Envía los datos formateados al tema 'users_created' en Kafka
            producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error occurred: {e}')  # Registra el error si ocurre alguno
            continue

# Define el DAG en Airflow
with DAG('user_automation', default_args=default_args, schedule='@daily', catchup=False) as dag:
    # Crea una tarea en Airflow que ejecutará la función 'stream_data'
    streaming_task = PythonOperator(
        task_id='stream_data_from_api',  # Identificador único para la tarea
        python_callable=stream_data  # Función que será llamada por la tarea
    )

stream_data()