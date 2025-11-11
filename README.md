# Explicaciíon
El diseño del microservicio se modificaría para incluir una capa adicional de comunicación entre microservicios: 

* Comunicación entre microservicios:
El microservicio de cálculo de factorial seguiría realizando el mismo cálculo, pero, una vez calculado el resultado, necesitaría enviar los datos (número recibido, factorial y etiqueta "par/impar") al microservicio de historial, que se encargaría de almacenar esta información en una base de datos externa. Esta comunicación entre microservicios se realizaría a través de solicitudes HTTP (por ejemplo, utilizando el método POST).

* Nuevo Servicio de Historial:
El microservicio de historial debería estar configurado para recibir datos de otros servicios (en este caso, el microservicio de cálculo), procesarlos y almacenarlos en una base de datos externa. Este servicio debe tener una API REST que permita recibir solicitudes POST con los datos de los cálculos y guardarlos en la base de datos.

* Almacenamiento Externo:
El microservicio de historial almacenará los datos de cada cálculo (número, factorial y la etiqueta "par/impar") en una base de datos externa. Esto podría ser una base de datos SQL (como MySQL o PostgreSQL) o NoSQL (como MongoDB), dependiendo de los requisitos del sistema.

-----------------------------------------------------------------------
## Flujo Modificado del Microservicio

1. Solicitud Inicial: El microservicio de cálculo recibe un número en la URL
2. Cálculo del Factorial: Calcula el factorial y determina si el factorial es par o impar
3. Envío de Datos a Historial: Después de calcular el factorial, el microservicio de cálculo hace una solicitud POST al microservicio de historial, enviando los datos del cálculo (número, factorial y par/impar).
4. Despues el almacenamiento en la Base de Datos: El microservicio de historial recibe los datos y los almacena en una base de datos externa.
5. Respuesta: El microservicio de cálculo puede responder con una confirmación o un mensaje de éxito.

-----------------------------------------------------------------------
## Modificar el Microservicio de Cálculo:

import requests
import math

def calcular_y_guardar_factorial(numero):
    
    resultado_factorial = math.factorial(numero)
    
    es_par = 'par' if resultado_factorial % 2 == 0 else 'impar'
    
    guardar_calculo_en_historial(numero, resultado_factorial, es_par)

def guardar_calculo_en_historial(numero, resultado_factorial, es_par):
    
    url_historial = "http://direccion_del_servicio_historial/api/historial"
    
        datos = {
        "numero": numero,
        "factorial": resultado_factorial,
        "par_impar": es_par
    }
    
    # Realizar una solicitud POST para almacenar los resultados
    respuesta = requests.post(url_historial, json=datos)
    
    if respuesta.status_code == 200:
        print("Cálculo guardado con éxito en el historial")
    else:
        print("Error al guardar el cálculo en el historial")


### Crear el Microservicio de Historial:

Este microservicio debe tener un endpoint que reciba las solicitudes POST y almacene los datos en la base de datos. Aquí es donde se guardarán los cálculos (número, factorial y si es par o impar).

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@localhost/historial_db'
db = SQLAlchemy(app)

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    factorial = db.Column(db.Integer, nullable=False)
    par_impar = db.Column(db.String(4), nullable=False)

@app.route('/api/historial', methods=['POST'])
def guardar_historial():
    data = request.get_json()

    numero = data['numero']
    factorial = data['factorial']
    par_impar = data['par_impar']

    nuevo_calculo = Historial(numero=numero, factorial=factorial, par_impar=par_impar)

    try:
        db.session.add(nuevo_calculo)
        db.session.commit()
        return jsonify({"message": "Cálculo guardado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al guardar el cálculo", "error": str(e)}), 500

if __name__ == '__main__':
    db.create_all()  

    app.run(debug=True)

