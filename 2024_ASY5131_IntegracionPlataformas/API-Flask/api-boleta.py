from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Api, Resource
import requests
#from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)
#api = Api(app)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#            host           / endpoint
#url = "http://localhost:7777/api/cliente"
#url1 = "http://localhost:5000/api/producto"

carrito = {
    'cliente': '',
    'items': [],
    'metodo_pago': '',
    'forma_envio': ''
}


# calcular el total carrito
def calcular_total(items):
    return sum(item['precio'] * item['cantidad'] for item in items)

#  factura en  HTML
@app.route('/carrito', methods=['GET'])
def mostrar_carrito():
    total = calcular_total(carrito['items'])
    return render_template('carrito.html', carrito=carrito, total=total)

#agregar un item al carrito
@app.route('/agregar_item', methods=['GET', 'POST'])
def agregar_item():
    if request.method == 'POST':
        cliente_razonSocial = request.form['cliente']
        producto_nombreproducto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        metodo_pago = request.form['metodo_pago']
        forma_envio = request.form['forma_envio']

        
        # obtener los datos del cliente
        cliente_response = requests.get(f'http://localhost:7777/api/cliente/{cliente_razonSocial}')
        cliente_data = cliente_response.json()
        carrito['cliente'] = cliente_data['razonSocial']

        #  para obtener los datos del producto
        cliente_response = requests.get(f'http://localhost:5000/api/producto/{producto_nombreproducto}')
        cliente_data = cliente_response.json()
        carrito['Producto'] = cliente_data['nombreproducto']
        
        #  para obtener los datos del producto
        producto_response = requests.get(f'http://localhost:5000/api/producto/{producto_nombreproducto}')
        producto_data = producto_response.json()
        producto_data['cantidad'] = cantidad
        
        carrito['items'].append(producto_data)
        carrito['metodo_pago'] = metodo_pago
        carrito['forma_envio'] = forma_envio

        #carrito['fecha_hora'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        return redirect(url_for('mostrar_carrito'))
    
    # obtener lista de clientes y productos
    clientes_response = requests.get('http://localhost:7777/api/cliente/')
    productos_response = requests.get('http://localhost:5000/api/producto/')
    clientes = clientes_response.json()
    productos = productos_response.json()
    
    return render_template('agregar_item.html', clientes=clientes, productos=productos)

@app.route('/factura', methods=['GET'])
def mostrar_factura():
    total = calcular_total(carrito['items'])
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('factura.html', carrito=carrito, total=total, fecha_hora=fecha_hora)

if __name__ == '__main__':
    app.run(debug=True)




