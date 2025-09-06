import streamlit as st
import numpy as np
import time # Para simular la captura de datos
# Asume que las funciones y el modelo están definidos en otro archivo o aquí mismo
# from your_model_file import preprocess_ppg_signal, create_model, predict_rhythm

# --- Mock-up de las funciones del modelo para demostración ---
# En una aplicación real, estas funciones vendrían de tu código de ML
def preprocess_ppg_signal(signal, fs=25):
    # Simulación de preprocesamiento: devuelve una señal con la forma esperada
    target_length = 1500
    if len(signal) > target_length:
        processed_signal = signal[:target_length]
    elif len(signal) < target_length:
        processed_signal = np.pad(signal, (0, target_length - len(signal)), 'constant')
    else:
        processed_signal = signal
    processed_signal = np.expand_dims(processed_signal, axis=-1)
    processed_signal = np.expand_dims(processed_signal, axis=0)
    return processed_signal

# Mock-up de un modelo pre-entrenado
class MockModel:
    def predict(self, data):
        # Simula una predicción: 0 = Normal, 1 = Arritmia, 2 = Fibrilación
        # Esto sería el resultado real de tu modelo Keras
        return np.array([[0.8, 0.1, 0.1]]) # 80% de probabilidad de ser Normal

mock_model = MockModel()

def predict_rhythm(signal_data, model):
    processed_data = preprocess_ppg_signal(signal_data)
    prediction = model.predict(processed_data)
    return np.argmax(prediction)
# --- Fin Mock-up ---


st.set_page_config(layout="centered", page_title="Monitor Cardíaco Smartwatch")

st.title("🫀 Monitor de Ritmo Cardíaco (Smartwatch)")
st.markdown("""
Esta aplicación simula el análisis del ritmo cardíaco usando datos de PPG de un smartwatch.
Pulsa 'Iniciar Monitoreo' para comenzar la captura y el análisis.
""")

# Área para mostrar el estado y los resultados
st.sidebar.header("Opciones de Monitoreo")
start_button = st.sidebar.button("▶️ Iniciar Monitoreo")
stop_button = st.sidebar.button("⏹️ Detener Monitoreo")

# Placeholder para actualizar el estado en tiempo real
status_placeholder = st.empty()
hr_placeholder = st.empty()
rhythm_placeholder = st.empty()
chart_placeholder = st.empty()


if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False

if start_button:
    st.session_state.monitoring_active = True

if stop_button:
    st.session_state.monitoring_active = False
    st.sidebar.success("Monitoreo detenido.")


if st.session_state.monitoring_active:
    status_placeholder.info("Monitoreo activo... Capturando datos del smartwatch.")

    # Simulación de captura de datos PPG (en un caso real, esto vendría del dispositivo)
    # Generamos una señal PPG ruidosa para simular datos reales
    fs = 25 # Frecuencia de muestreo (25 Hz)
    duration = 5 # Duración de la captura en segundos
    num_samples = fs * duration
    time_series = np.linspace(0, duration, num_samples)

    # Simula una señal PPG con un ritmo "normal" pero con ruido
    # Frecuencia cardíaca de 70 lpm (aprox 1.16 Hz)
    ppg_signal = 0.5 * np.sin(2 * np.pi * 1.16 * time_series) + \
                 0.2 * np.sin(2 * np.pi * 2.32 * time_series) + \
                 0.1 * np.random.randn(num_samples) # Ruido

    # Aquí se llamarían tus funciones reales de ML
    rhythm_class = predict_rhythm(ppg_signal, mock_model)

    # Mapeo de resultados a texto legible
    rhythm_labels = {0: "Normal", 1: "Arritmia detectada", 2: "Fibrilación Auricular"}
    result_text = rhythm_labels.get(rhythm_class, "Desconocido")

    # Simular un cálculo de HR
    simulated_hr = np.random.randint(60, 100) # Frecuencia cardíaca simulada

    # Actualizar los placeholders
    hr_placeholder.metric(label="Frecuencia Cardíaca (BPM)", value=f"{simulated_hr}")

    if rhythm_class == 0:
        rhythm_placeholder.success(f"**Ritmo Cardíaco:** {result_text} ✅")
    else:
        rhythm_placeholder.error(f"**Ritmo Cardíaco:** {result_text} 🚨 **¡Consulta a un médico!**")

    # Graficar la señal PPG (solo una parte para visualización)
    chart_placeholder.subheader("Señal PPG Capturada")
    st.line_chart(ppg_signal[-500:]) # Mostrar los últimos 500 puntos para que sea legible

    # Pequeña pausa para simular el monitoreo continuo
    time.sleep(1)
    st.rerun() # Actualiza la página para simular monitoreo en tiempo real