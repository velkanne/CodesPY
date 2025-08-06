
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Usar un backend de Matplotlib que no requiera GUI
matplotlib.use('Agg')

def scraper_y_visualizador():
    """
    Función principal que extrae datos y genera una visualización.
    """
    # --- 1. Web Scraping ---
    print("Iniciando scraping de la portada de Wikipedia en español...")
    url = "https://es.wikipedia.org/wiki/Wikipedia:Portada"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza un error si la petición no fue exitosa (código 200)
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página: {e}")
        return

    # Analizar el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # Encontrar todos los titulares. Usamos selectores CSS para buscar etiquetas h1, h2, h3, etc.
    # que estén dentro del área de contenido principal de Wikipedia.
    titulares_tags = soup.select('#bodyContent #mw-content-text .mw-headline')
    
    if not titulares_tags:
        print("No se encontraron titulares con el selector esperado. La estructura de la página pudo haber cambiado.")
        return

    titulares_texto = [tag.get_text(strip=True) for tag in titulares_tags]
    print(f"Se encontraron {len(titulares_texto)} titulares.")

    # --- 2. Procesamiento y Visualización ---
    print("Procesando datos para la visualización...")
    # Crear un DataFrame de Pandas para manejar los datos fácilmente
    df = pd.DataFrame({
        'Titular': titulares_texto,
        'Longitud': [len(t) for t in titulares_texto]
    })

    # Filtrar titulares vacíos si los hubiera
    df = df[df['Longitud'] > 0]

    # Ordenar por longitud para un gráfico más limpio
    df = df.sort_values(by='Longitud', ascending=False).head(10) # Tomar solo los 10 más largos

    print("Generando gráfico de barras...")
    # Crear el gráfico
    plt.figure(figsize=(12, 8)) # Tamaño de la figura
    plt.barh(df['Titular'], df['Longitud'], color='skyblue') # Gráfico de barras horizontal
    plt.xlabel('Longitud del Titular (número de caracteres)')
    plt.ylabel('Titulares')
    plt.title('Top 10 Titulares más Largos de la Portada de Wikipedia (Español)')
    plt.gca().invert_yaxis() # Invertir el eje Y para que el más largo aparezca arriba
    plt.tight_layout() # Ajustar para que no se corten las etiquetas

    # Guardar el gráfico en un archivo
    nombre_archivo = "grafico_titulares.png"
    plt.savefig(nombre_archivo)
    
    print(f"¡Éxito! El gráfico ha sido guardado como '{nombre_archivo}'")

if __name__ == "__main__":
    scraper_y_visualizador()
