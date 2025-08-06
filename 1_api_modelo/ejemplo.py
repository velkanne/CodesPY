
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# --- Simulación de un Modelo de Machine Learning ---
# En un proyecto real, aquí cargarías tu modelo entrenado (por ejemplo, desde un archivo .pkl)
# from joblib import load
# model = load('mi_modelo_entrenado.pkl')

class ModeloSimulado:
    """Un modelo falso que "predice" el precio de una casa basado en sus características."""
    def predict(self, datos):
        # Fórmula simple: 15000 * metros_cuadrados + 5000 * habitaciones - 2000 * antiguedad
        precios = []
        for dato in datos:
            precio = 15000 * dato[0] + 5000 * dato[1] - 2000 * dato[2]
            precios.append(precio)
        return np.array(precios)

model = ModeloSimulado()
# --- Fin de la Simulación ---


# --- Definición de la API con FastAPI ---
app = FastAPI(
    title="API de Predicción de Precios de Casas",
    description="Una API para simular la predicción del valor de una propiedad."
)

# Pydantic nos ayuda a definir la estructura de los datos de entrada
class DatosCasa(BaseModel):
    metros_cuadrados: float
    habitaciones: int
    antiguedad_anios: int

    class Config:
        schema_extra = {
            "example": {
                "metros_cuadrados": 120,
                "habitaciones": 3,
                "antiguedad_anios": 5
            }
        }

@app.post("/predecir")
def predecir_precio(datos: DatosCasa):
    """
    Recibe los datos de una casa y devuelve una predicción de su precio.
    """
    # Convertir los datos de entrada al formato que el modelo espera (un array de NumPy)
    datos_modelo = np.array([[
        datos.metros_cuadrados,
        datos.habitaciones,
        datos.antiguedad_anios
    ]])

    # Realizar la predicción
    prediccion = model.predict(datos_modelo)

    # Devolver el resultado en un formato JSON claro
    return {
        "prediccion_precio_estimado": f"${prediccion[0]:,.2f} USD",
        "datos_recibidos": datos
    }

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API de predicción. Ve a /docs para probarla."}
