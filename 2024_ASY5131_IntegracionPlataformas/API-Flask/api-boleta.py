from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Api, Resource
import requests
#from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://Salazar:Dethklok1470@proyectoapi.database.windows.net/PROYECTO?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    items = db.Column(db.Text, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pago = db.Column(db.String(50))
    forma_envio = db.Column(db.String(50))
    total = db.Column(db.Float)
    estado = db.Column(db.String(50))

carrito = {
    'cliente': '',
    'items': [],
    'metodo_pago': '',
    'forma_envio': ''
}

facturas=[]
id_factura = 0


# calcular el total carrito
def calcular_total(items):
    return sum(item['precio'] * item['cantidad'] for item in items)

#  carrito en  HTML
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
    factura = {
        'id': len(facturas) + 1,
        'cliente': carrito['cliente'],
        'items': carrito['items'],
        'metodo_pago': carrito['metodo_pago'],
        'forma_envio': carrito['forma_envio'],
        'total': total,
        'fecha_hora': fecha_hora,
        'estado': 'Pendiente'
    }
    facturas.append(factura)


    # Guardar factura en Base de datos 
    nueva_factura = Factura(
        cliente=factura['cliente'],
        items=str(factura['items']),  
        fecha_hora=datetime.now(),
        metodo_pago=factura['metodo_pago'],
        forma_envio=factura['forma_envio'],
        total=factura['total'],
        estado=factura['estado']
    )

    db.session.add(nueva_factura)
    db.session.commit()
   

    requests.post('http://localhost:6000/api/pedido', json={
        'Id': factura['id'],
        'Estado': factura['estado']
    })


    # actualiza estock 
    for item in carrito['items']:
        producto_id = item['id']
        cantidad = item['cantidad']
        requests.put(f'http://localhost:5000/api/producto/{producto_id}/DescuentoStock', json=cantidad)

        requests.post('http://localhost:6000/api/pedido', json=factura)


    # Limpiar el carrito cuando genere la facura
    carrito['items'] = []
    carrito['metodo_pago'] = ''
    carrito['forma_envio'] = ''



    return render_template('factura.html', factura=factura, carrito=carrito, total=total, fecha_hora=fecha_hora )


@app.route('/eliminar_factura/<int:index>', methods=['POST'])
def eliminar_factura(index):
    if 0 <= index < len(facturas):
        del facturas[index]
    return redirect(url_for('vista_bodeguero'))

@app.route('/actualizar_estado/<int:id>', methods=['POST'])
def actualizar_estado(id):
    nuevo_estado = request.form['estado']
    response = requests.put(f'http://localhost:6000/api/pedido/{id}', json={'estado': nuevo_estado})
    if response.status_code == 200:
        for factura in facturas:
            if factura['id'] == id:
                factura['estado'] = nuevo_estado
                break
        return redirect(url_for('vista_bodeguero'))
    else:
        # Hubo un error
        return f"Error al actualizar el estado: {response.status_code}", response.status_code

@app.route('/bodeguero', methods=['GET'])
def vista_bodeguero():
    return render_template('bodeguero.html', facturas=facturas)





if __name__ == '__main__':
    app.run(debug=True)




