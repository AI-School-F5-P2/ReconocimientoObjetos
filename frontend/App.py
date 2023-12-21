import streamlit as st
import pandas as pd
import numpy as np
import requests




st.title('Detección de logos/marcas')

#variables y funciones
DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)  # Carga el conjunto de datos desde la URL usando Pandas
    lowercase = lambda x: str(x).lower()  # Define una función lambda para convertir los nombres de las columnas a minúsculas
    data.rename(lowercase, axis='columns', inplace=True)  # Aplica la función lambda a los nombres de las columnas
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])  # Convierte la columna de fecha/hora a formato datetime
    return data  # Devuelve el conjunto de datos modificado

# Cargar el conjunto de datos
data_load_state = st.text('Cargando datos...')
data = load_data(10000)
data_load_state.text('Datos cargados correctamente!')

# Función para verificar si la URL es un enlace válido de YouTube
def es_enlace_youtube(url):
    return "youtube.com" in url or "youtu.be" in url

#sección para mostrar el video
video_url = st.text_input('Insertar URL del video')


if video_url:
    if es_enlace_youtube(video_url):
        st.success("El enlace es válido.")
        st.video(video_url)

        # Botón para guardar los resultados en MongoDB
        if st.button('Guardar resultados en MongoDB'):
            # Prepara los datos que deseas enviar a Flask
            data_to_send = {
                'video_url': video_url,
                # Puedes agregar más datos si es necesario
            }

            # Envía los datos al servidor Flask
            response = requests.post('http://localhost:5000/upload_videos', json=data_to_send)

            # Verifica si la solicitud se completó con éxito
            if response.status_code == 200:
                st.success('Resultados guardados exitosamente en MongoDB')
            else:
                st.error('Error al guardar los resultados en MongoDB')
    else:
        st.error("El enlace no es válido. Por favor, introduce un enlace válido de YouTube.")

#muestra el video
if video_url:
    st.video(video_url)




