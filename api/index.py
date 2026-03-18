from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Usar memoria (Vercel no guarda archivos)
solicitudes_db = []

def generar_codigo():
    ahora = datetime.now()
    return f"SOL-{ahora.year}-{ahora.month:02d}{ahora.day:02d}-{len(solicitudes_db)+1:04d}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/solicitudes', methods=['POST'])
def crear():
    data = request.json
    codigo = generar_codigo()
    
    solicitud = {
        'numero': codigo,
        'fecha': datetime.now().isoformat(),
        'nombre': data.get('nombre'),
        'cedula': data.get('cedula'),
        'email': data.get('email'),
        'estado': 'pendiente'
    }
    
    solicitudes_db.append(solicitud)
    return jsonify({'success': True, 'codigo': codigo})

@app.route('/api/solicitudes/<cedula>', methods=['GET'])
def consultar(cedula):
    resultados = [s for s in solicitudes_db if s['cedula'] == cedula]
    return jsonify({'success': True, 'data': resultados})

# Exportar para Vercel
app = app