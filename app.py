from flask import Flask, jsonify
import math

app = Flask(__name__)

@app.route('/factorial/<int:num>', methods=['GET'])
def calcular_factorial(num):
    factorial = math.factorial(num)
    
    par_impar = 'par' if num % 2 == 0 else 'impar'
    
    response = {
        'numero_recibido': num,
        'factorial': factorial,
        'par_impar': par_impar
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

