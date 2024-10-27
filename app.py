import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json

def on_publish(client, userdata, result):  # create function for callback
    print("¡El dato ha sido publicado! 🎉\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración de MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("icorreav2")
client1.on_message = on_message

# Cambiar el color de fondo
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f8ff;  /* Color de fondo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título y subtítulo
st.title("🌟 Interfaces Multimodales 🌟")
st.subheader("CONTROL POR VOZ")

# Cargar y mostrar imagen
image = Image.open('voice.png')
st.image(image, width=400)

# Barra lateral para instrucciones
with st.sidebar:
    st.header("Instrucciones")
    st.write("1. Haz clic en el botón 'Inicio'.")
    st.write("2. Habla claramente al micrófono.")
    st.write("3. La aplicación reconocerá tu voz y publicará el mensaje.")
    st.write("4. Verifica los resultados en la pantalla.")

# Mensaje para interactuar
st.write("🔊 Toca el botón y habla: ")

# Botón para iniciar reconocimiento de voz
stt_button = Button(label="🗣️ Inicio", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.markdown(f"<h4 style='color: blue;'>Reconocido: {result.get('GET_TEXT')}</h4>", unsafe_allow_html=True)
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": result.get("GET_TEXT").strip()})
        ret = client1.publish("datos_voz_icov", message)

    try:
        os.mkdir("temp")
    except:
        pass

    
    try:
        os.mkdir("temp")
    except:
        pass
