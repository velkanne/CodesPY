
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_muy_segura!' # Clave para proteger las sesiones
socketio = SocketIO(app, async_mode='eventlet')

# --- Frontend: Página HTML con JavaScript para el cliente ---
# En un proyecto más grande, esto estaría en un archivo .html separado.
HTML_CLIENTE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat en Tiempo Real</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; }
        #mensajes { list-style-type: none; padding: 0; border: 1px solid #ccc; height: 300px; overflow-y: scroll; margin-bottom: 10px; }
        #mensajes li { padding: 8px; border-bottom: 1px solid #eee; }
        #formulario { display: flex; }
        #input_mensaje { flex-grow: 1; padding: 10px; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h2>Chat Básico en Tiempo Real</h2>
    <ul id="mensajes"></ul>
    <form id="formulario" action="" onsubmit="enviarMensaje(event)">
        <input id="input_mensaje" autocomplete="off" placeholder="Escribe un mensaje..."/>
        <button>Enviar</button>
    </form>

    <script type="text/javascript">
        // Conectarse al servidor de Socket.IO
        var socket = io();

        // Cuando se recibe un evento 'connect', registrar en la consola
        socket.on('connect', function() {
            console.log('Conectado al servidor!');
        });

        // Cuando se recibe un evento 'nuevo_mensaje', añadirlo a la lista de mensajes
        socket.on('nuevo_mensaje', function(datos) {
            var item = document.createElement('li');
            item.textContent = datos.usuario + ': ' + datos.msg;
            document.getElementById('mensajes').appendChild(item);
            window.scrollTo(0, document.body.scrollHeight); // Auto-scroll hacia abajo
        });

        // Función para enviar un mensaje al servidor
        function enviarMensaje(event) {
            event.preventDefault(); // Evitar que la página se recargue
            var input = document.getElementById('input_mensaje');
            if (input.value) {
                socket.emit('enviar_mensaje', {msg: input.value});
                input.value = ''; // Limpiar el campo de texto
            }
        }
    </script>
</body>
</html>
'''

# --- Backend: Lógica del Servidor Flask ---

@app.route('/')
def index():
    """Sirve la página principal del chat."""
    return render_template_string(HTML_CLIENTE)

@socketio.on('connect')
def al_conectar():
    """Se ejecuta cuando un nuevo cliente se conecta."""
    print("¡Un cliente se ha conectado!")
    # Notificar a todos los clientes que alguien se unió
    emit('nuevo_mensaje', {'usuario': 'Sistema', 'msg': 'Un nuevo usuario se ha unido al chat.'}, broadcast=True)

@socketio.on('enviar_mensaje')
def manejar_mensaje(json):
    """Se ejecuta cuando el servidor recibe un mensaje de un cliente."""
    print(f"Mensaje recibido: {json['msg']}")
    # Reenviar el mensaje a TODOS los clientes conectados
    emit('nuevo_mensaje', {'usuario': 'Anónimo', 'msg': json['msg']}, broadcast=True)

@socketio.on('disconnect')
def al_desconectar():
    """Se ejecuta cuando un cliente se desconecta."""
    print("¡Un cliente se ha desconectado!")

if __name__ == '__main__':
    print("Iniciando servidor de chat en http://127.0.0.1:5000")
    # Usar socketio.run para iniciar el servidor correctamente
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
