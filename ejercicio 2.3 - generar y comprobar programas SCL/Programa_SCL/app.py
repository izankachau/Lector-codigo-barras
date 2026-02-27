from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from database import init_db

app = Flask(__name__)

init_db()

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'scl_library.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/programs', methods=['GET'])
def get_programs():
    conn = get_db_connection()
    programs = conn.execute('SELECT * FROM scl_programs ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(p) for p in programs])

@app.route('/api/programs', methods=['POST'])
def save_program():
    data = request.json
    conn = get_db_connection()
    if data.get('id'):
        conn.execute('UPDATE scl_programs SET name=?, category=?, code=?, description=? WHERE id=?',
                     (data['name'], data['category'], data['code'], data['description'], data['id']))
    else:
        conn.execute('INSERT INTO scl_programs (name, category, code, description) VALUES (?,?,?,?)',
                     (data['name'], data['category'], data['code'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Plantilla guardada correctamente."})

@app.route('/api/programs/<int:id>', methods=['DELETE'])
def delete_program(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM scl_programs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Plantilla eliminada."})

@app.route('/api/check', methods=['POST'])
def check_scl():
    data = request.json
    code = data.get('code', '')
    errors = []
    
    lines = code.split('\n')
    stack_if = []
    stack_for = []
    
    for i, line in enumerate(lines):
        ln = i + 1
        cnt = line.strip()
        if not cnt or cnt.startswith('//'): continue

        # 1. Comprobación de Punto y Coma
        no_semi_keywords = ['IF', 'THEN', 'ELSE', 'ELSIF', 'FOR', 'DO', 'WHILE', 'CASE', 'OF', 'BEGIN', 'VAR', 'END_VAR']
        if not cnt.endswith(';') and not any(cnt.upper().startswith(kw) for kw in no_semi_keywords) and not any(cnt.upper() == kw for kw in ['END_IF', 'END_FOR', 'END_WHILE', 'END_CASE']):
            errors.append({
                "line": ln,
                "type": "Error de Sintaxis",
                "desc": "Falta el punto y coma ';' al final de la instrucción.",
                "fix": "Añade ';' al final de la línea para cerrar la sentencia."
            })

        # 2. Control de bloques IF
        if 'IF ' in cnt.upper() and 'THEN' in cnt.upper(): stack_if.append(ln)
        if 'END_IF' in cnt.upper():
            if not stack_if:
                errors.append({"line": ln, "type": "Error Logico", "desc": "END_IF sin un IF previo.", "fix": "Elimina este END_IF o añade la apertura IF correspondiente."})
            else: stack_if.pop()

        # 3. Control de bloques FOR
        if 'FOR ' in cnt.upper() and 'DO' in cnt.upper(): stack_for.append(ln)
        if 'END_FOR' in cnt.upper():
            if not stack_for:
                errors.append({"line": ln, "type": "Error Logico", "desc": "END_FOR sin un FOR previo.", "fix": "Elimina este END_FOR o añade la apertura FOR correspondiente."})
            else: stack_for.pop()

    # Comprobar bloques no cerrados
    for start_ln in stack_if:
        errors.append({"line": start_ln, "type": "Bloque Abierto", "desc": "Sentencia IF no cerrada.", "fix": "Añade un END_IF; al final de la lógica del bloque."})
    for start_ln in stack_for:
        errors.append({"line": start_ln, "type": "Bloque Abierto", "desc": "Bucle FOR no cerrado.", "fix": "Añade un END_FOR; al final del bucle."})

    if not errors:
        return jsonify({"status": "success", "message": "Analizador: Código SCL perfecto e industrial."})
    else:
        return jsonify({"status": "warning", "message": "Se han detectado irregularidades técnicas.", "errors": errors})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
