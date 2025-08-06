import random
import string

class AcortadorURL:
    """
    Clase que maneja la lógica para acortar y expandir URLs.
    """
    def __init__(self):
        # En un proyecto real, esto sería una conexión a una base de datos.
        # Usamos dos diccionarios para búsquedas rápidas en ambas direcciones.
        self.url_a_codigo = {}
        self.codigo_a_url = {}

    def _generar_codigo(self, longitud=6):
        """Genera un código alfanumérico aleatorio y único."""
        caracteres = string.ascii_letters + string.digits
        while True:
            codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
            # Asegurarse de que el código no exista ya
            if codigo not in self.codigo_a_url:
                return codigo

    def acortar(self, url_larga):
        """
        Acorta una URL larga. Si ya fue acortada, devuelve el código existente.
        """
        if not url_larga.startswith(('http://', 'https://')):
            return None, "Error: La URL debe empezar con http:// o https://"

        if url_larga in self.url_a_codigo:
            codigo = self.url_a_codigo[url_larga]
            return f"http://miacortador.com/{codigo}", "Esta URL ya había sido acortada."
        
        codigo = self._generar_codigo()
        self.url_a_codigo[url_larga] = codigo
        self.codigo_a_url[codigo] = url_larga
        
        return f"http://miacortador.com/{codigo}", "URL acortada con éxito."

    def expandir(self, url_corta):
        """
        Expande una URL corta a su URL original.
        """
        try:
            codigo = url_corta.split('/')[-1]
        except IndexError:
            return None, "Error: Formato de URL corta no válido."

        if codigo in self.codigo_a_url:
            return self.codigo_a_url[codigo], "URL expandida con éxito."
        else:
            return None, "Error: Esta URL corta no existe en nuestro sistema."

def menu_interactivo():
    """Maneja la interfaz de usuario en la consola."""
    acortador = AcortadorURL()
    print("--- Bienvenido al Acortador de URLs de Consola ---")

    while True:
        print("\nOpciones:")
        print("1. Acortar una URL")
        print("2. Expandir una URL corta")
        print("3. Salir")
        
        eleccion = input("Elige una opción (1/2/3): ")

        if eleccion == '1':
            url_larga = input("Introduce la URL larga que quieres acortar: ")
            url_corta, mensaje = acortador.acortar(url_larga)
            print(f"\nResultado: {mensaje}")
            if url_corta:
                print(f"Tu URL corta es: {url_corta}")
        
        elif eleccion == '2':
            url_corta_input = input("Introduce la URL corta que quieres expandir: ")
            url_original, mensaje = acortador.expandir(url_corta_input)
            print(f"\nResultado: {mensaje}")
            if url_original:
                print(f"La URL original es: {url_original}")

        elif eleccion == '3':
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")

if __name__ == "__main__":
    menu_interactivo()
