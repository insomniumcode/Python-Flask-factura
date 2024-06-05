from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Api, Resource
import requests
from flask_cors import CORS



app = Flask(__name__)
#api = Api(app)
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#            host           / endpoint
#url = "http://localhost:7777/api/cliente"
#url1 = "http://localhost:5000/api/producto"

factura = {
    'cliente': '',
    'items': []
}


# Función para calcular el total de la factura
def calcular_total(items):
    return sum(item['precio'] * item['cantidad'] for item in items)

# Ruta para mostrar la factura en formato HTML
@app.route('/factura', methods=['GET'])
def mostrar_factura():
    total = calcular_total(factura['items'])
    return render_template('factura.html', factura=factura, total=total)

# Ruta para agregar un item a la factura
@app.route('/agregar_item', methods=['GET', 'POST'])
def agregar_item():
    if request.method == 'POST':
        cliente_razonSocial = request.form['cliente']
        producto_nombreproducto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        
        # Llamar a la API de C# para obtener los datos del cliente
        cliente_response = requests.get(f'http://localhost:7777/api/cliente/{cliente_razonSocial}')
        cliente_data = cliente_response.json()
        factura['cliente'] = cliente_data['razonSocial']

        cliente_response = requests.get(f'http://localhost:5000/api/producto/{producto_nombreproducto}')
        cliente_data = cliente_response.json()
        factura['Producto'] = cliente_data['nombreproducto']
        
        # Llamar a la API de C# para obtener los datos del producto
        producto_response = requests.get(f'http://localhost:5000/api/producto/{producto_nombreproducto}')
        producto_data = producto_response.json()
        producto_data['cantidad'] = cantidad
        
        factura['items'].append(producto_data)
        
        return redirect(url_for('mostrar_factura'))
    
    # Llamar a las APIs para obtener la lista de clientes y productos
    clientes_response = requests.get('http://localhost:7777/api/cliente/')
    productos_response = requests.get('http://localhost:5000/api/producto/')
    clientes = clientes_response.json()
    productos = productos_response.json()
    
    return render_template('agregar_item.html', clientes=clientes, productos=productos)

if __name__ == '__main__':
    app.run(debug=True)





