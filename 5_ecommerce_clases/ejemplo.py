

import datetime

class Producto:
    """Representa un artículo individual que se puede vender."""
    def __init__(self, id_producto, nombre, precio, stock=10):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    def __str__(self):
        return f"{self.nombre} (${self.precio:.2f}) - Stock: {self.stock}"

    def reducir_stock(self, cantidad=1):
        if self.stock >= cantidad:
            self.stock -= cantidad
            return True
        return False

class CarritoDeCompras:
    """Representa el carrito de un cliente."""
    def __init__(self):
        self.items = {} # {id_producto: {'producto': objeto_producto, 'cantidad': n}}

    def agregar_producto(self, producto, cantidad=1):
        if not isinstance(producto, Producto):
            print("Error: Solo se pueden agregar objetos de tipo Producto.")
            return

        if producto.stock < cantidad:
            print(f"No hay suficiente stock para '{producto.nombre}'. Disponible: {producto.stock}")
            return

        if producto.id_producto in self.items:
            self.items[producto.id_producto]['cantidad'] += cantidad
        else:
            self.items[producto.id_producto] = {'producto': producto, 'cantidad': cantidad}
        
        print(f"{cantidad} x '{producto.nombre}' agregado(s) al carrito.")

    def calcular_total(self):
        total = 0.0
        for item in self.items.values():
            total += item['producto'].precio * item['cantidad']
        return total

    def mostrar_carrito(self):
        if not self.items:
            print("El carrito está vacío.")
            return
        
        print("--- Contenido del Carrito ---")
        for item in self.items.values():
            p = item['producto']
            cantidad = item['cantidad']
            subtotal = p.precio * cantidad
            print(f"- {p.nombre}: {cantidad} x ${p.precio:.2f} = ${subtotal:.2f}")
        print("-----------------------------")
        print(f"Total del Carrito: ${self.calcular_total():.2f}")

class Pedido:
    """Representa un pedido finalizado por un cliente."""
    def __init__(self, carrito, direccion_envio):
        if not carrito.items:
            raise ValueError("No se puede crear un pedido de un carrito vacío.")

        self.fecha = datetime.datetime.now()
        self.items_pedido = carrito.items.copy() # Copiar los items en el momento de la compra
        self.total_pagado = carrito.calcular_total()
        self.direccion_envio = direccion_envio
        self.estado = "Procesando"

        # Actualizar el stock de los productos
        for item in self.items_pedido.values():
            item['producto'].reducir_stock(item['cantidad'])

    def mostrar_resumen_pedido(self):
        print("\n======= Resumen del Pedido =======")
        print(f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Dirección de Envío: {self.direccion_envio}")
        print(f"Estado: {self.estado}")
        print("Productos:")
        for item in self.items_pedido.values():
            p = item['producto']
            cantidad = item['cantidad']
            print(f"  - {p.nombre} (x{cantidad})")
        print(f"Total Pagado: ${self.total_pagado:.2f}")
        print("==================================")

# --- Simulación de uso ---
if __name__ == "__main__":
    # 1. Crear algunos productos disponibles en la tienda
    print("--- Creando inventario de la tienda ---")
    laptop = Producto(id_producto="PROD001", nombre="Laptop Pro 15", precio=1500.00, stock=5)
    teclado = Producto(id_producto="PROD002", nombre="Teclado Mecánico RGB", precio=120.50, stock=20)
    monitor = Producto(id_producto="PROD003", nombre="Monitor 4K 27 pulgadas", precio=450.00, stock=10)
    print(laptop)
    print(teclado)
    print(monitor)
    print("\n" + "-"*20 + "\n")

    # 2. Simular un cliente que añade productos a su carrito
    print("--- Un cliente empieza a comprar ---")
    mi_carrito = CarritoDeCompras()
    mi_carrito.agregar_producto(laptop, 1)
    mi_carrito.agregar_producto(teclado, 2)
    mi_carrito.agregar_producto(monitor, 1)
    print()
    mi_carrito.mostrar_carrito()
    print("\n" + "-"*20 + "\n")

    # 3. El cliente finaliza la compra (crea un pedido)
    print("--- El cliente finaliza la compra ---")
    try:
        direccion = "Calle Falsa 123, Ciudad Ejemplo, CP 08080"
        mi_pedido = Pedido(mi_carrito, direccion)
        mi_pedido.mostrar_resumen_pedido()
    except ValueError as e:
        print(f"Error al crear el pedido: {e}")
    
    print("\n" + "-"*20 + "\n")

    # 4. Verificar el stock actualizado después de la compra
    print("--- Inventario actualizado de la tienda ---")
    print(laptop)
    print(teclado)
    print(monitor)
