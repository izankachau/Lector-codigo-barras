import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'scl_library.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla para los programas SCL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scl_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            code TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Insertar algunos ejemplos iniciales si la tabla está vacía
    cursor.execute('SELECT COUNT(*) FROM scl_programs')
    if cursor.fetchone()[0] == 0:
        examples = [
            ('Control Motor Simple', 'Motores', 
             '// Control de Motor\nIF #Start AND NOT #Stop THEN\n    #Motor_On := TRUE;\nELSIF #Stop OR #Thermal_Error THEN\n    #Motor_On := FALSE;\nEND_IF;',
             'Lógica básica de marcha/paro con protección térmica.'),
            ('Escalado Analógico', 'Procesos',
             '// Escalado de 0-27648 a Unidades de Ingeniería\n#Out_Val := ((#In_Raw - 0) / (27648 - 0)) * (#Max_Scale - #Min_Scale) + #Min_Scale;',
             'Cálculo matemático para normalizar señales analógicas.')
        ]
        cursor.executemany('INSERT INTO scl_programs (name, category, code, description) VALUES (?,?,?,?)', examples)
        
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()
