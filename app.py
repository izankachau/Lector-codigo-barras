import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from database import init_db, get_item, add_item, DB_PATH
import sqlite3
import threading
from playsound import playsound

# Configuración inicial
SCAN_RESULTS_DIR = "ResultadosEscaneo"
ASSETS_DIR = "assets"
SOUND_SUCCESS = os.path.join(ASSETS_DIR, "success.mp3")
SOUND_REGISTER = os.path.join(ASSETS_DIR, "register.mp3")

if not os.path.exists(SCAN_RESULTS_DIR): os.makedirs(SCAN_RESULTS_DIR)
if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)

init_db()

# Variables para control de sonido globales
last_sound_time = 0
last_beeped_code = None # Para evitar que suene repetidamente mientras se mantiene el mismo codigo
SOUND_COOLDOWN = 1.0

def play_audio(file_path):
    """Reproduce un sonido en un hilo separado para no congelar la cámara"""
    if os.path.exists(file_path):
        threading.Thread(target=playsound, args=(file_path,), daemon=True).start()

def get_all_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT code, name FROM inventory")
    items = cursor.fetchall()
    conn.close()
    return items

def draw_ui(frame, registered_items, highlighted_code=None, status_msg="Buscando...", progress=0):
    h, w, _ = frame.shape
    ui_width = w * 2
    canvas = np.zeros((h, ui_width, 3), dtype=np.uint8)
    canvas.fill(30) 

    # 1. Cámara (IZQUIERDA)
    canvas[0:h, 0:w] = frame

    # 2. Panel DERECHO
    panel_x = w
    
    # --- SUPERIOR: LISTA ---
    cv2.rectangle(canvas, (panel_x + 10, 10), (ui_width - 10, h // 2 - 5), (50, 50, 50), -1)
    cv2.putText(canvas, "PRODUCTOS REGISTRADOS", (panel_x + 20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    y_offset = 70
    max_items = (h // 2 - 80) // 30
    for i, (code, name) in enumerate(registered_items[:max_items]):
        color = (200, 200, 200)
        bg_color = (60, 60, 60)
        if code == highlighted_code:
            color = (0, 255, 0)
            bg_color = (0, 100, 0)
            cv2.rectangle(canvas, (panel_x + 15, y_offset - 20), (ui_width - 15, y_offset + 10), bg_color, -1)
        cv2.putText(canvas, f"{name} ({code})", (panel_x + 25, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        y_offset += 30

    # --- INFERIOR: ESTADO ---
    cv2.rectangle(canvas, (panel_x + 10, h // 2 + 5), (ui_width - 10, h - 10), (45, 45, 45), -1)
    cv2.putText(canvas, "ESTADO Y REGISTRO", (panel_x + 20, h // 2 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    color_status = (255, 255, 255)
    if "REGISTRAR" in status_msg: color_status = (0, 165, 255)
    if "DETECTADO" in status_msg: color_status = (0, 255, 0)
    cv2.putText(canvas, status_msg, (panel_x + 20, h // 2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_status, 2)
    
    # Barra Progreso
    bar_x1, bar_y1 = panel_x + 30, h - 60
    bar_x2, bar_y2 = ui_width - 30, h - 40
    cv2.rectangle(canvas, (bar_x1, bar_y1), (bar_x2, bar_y2), (100, 100, 100), 1)
    if progress > 0:
        fill_w = int((bar_x2 - bar_x1) * (progress / 100))
        cv2.rectangle(canvas, (bar_x1, bar_y1), (bar_x1 + fill_w, bar_y2), (0, 165, 255), -1)

    return canvas

def ask_user(title, prompt):
    root = tk.Tk()
    root.withdraw()
    result = simpledialog.askstring(title, prompt)
    root.destroy()
    return result

def main():
    global last_sound_time, last_beeped_code
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return

    last_detected_code = None
    detection_start_time = None
    db_cache = {}
    
    registered_items = get_all_items()
    for code, name in registered_items: db_cache[code] = name

    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        
        status_msg = "Buscando codigos..."
        highlighted_code = None
        progress = 0
        
        if barcodes:
            target_code = barcodes[0].data.decode('utf-8')
            
            # Dibujar y procesar cada codigo
            for barcode in barcodes:
                code_text = barcode.data.decode('utf-8')
                (x, y, w, h) = barcode.rect
                name = db_cache.get(code_text)
                
                if name:
                    color = (0, 255, 0)
                    display = f"PRODUCTO: {name}"
                    highlighted_code = code_text
                    status_msg = f"DETECTADO: {name}"
                    
                    # LOGICA DE SONIDO REFORZADA: 
                    # 1. Beep solo si es la PRIMERA VEZ que vemos este codigo en este "sighting"
                    # 2. Y solo si ha pasado mas de 1 segundo desde CUALQUIER beep anterior
                    current_time = time.time()
                    if code_text != last_beeped_code and (current_time - last_sound_time >= SOUND_COOLDOWN):
                        play_audio(SOUND_SUCCESS)
                        last_sound_time = current_time
                        last_beeped_code = code_text
                else:
                    color = (0, 165, 255)
                    display = f"DESCONOCIDO: {code_text}"
            
            # Lógica Registro para codigos nuevos
            if not db_cache.get(target_code):
                if target_code == last_detected_code:
                    if detection_start_time is None: detection_start_time = time.time()
                    elapsed = time.time() - detection_start_time
                    progress = min(100, int(elapsed * 100))
                    status_msg = f"Manten para registrar: {target_code}"
                    
                    if elapsed >= 1.0:
                        status_msg = "REGISTRANDO..."
                        full_ui = draw_ui(frame, registered_items, highlighted_code, status_msg, 100)
                        cv2.imshow('Lector Barcode Vision Expert', full_ui)
                        cv2.waitKey(1)
                        
                        if messagebox.askyesno("Nuevo Producto", f"El codigo {target_code} no esta registrado.\n¿Registrar ahora?"):
                            name = ask_user("Registrar", "Nombre del producto:")
                            if name:
                                desc = ask_user("Registrar", "Descripcion (opcional):") or "Sin descripcion"
                                add_item(target_code, name, desc)
                                play_audio(SOUND_REGISTER)
                                db_cache[target_code] = name
                                registered_items = get_all_items()
                                messagebox.showinfo("Exito", f"'{name}' guardado.")
                        
                        detection_start_time = None
                        last_detected_code = None
                else:
                    last_detected_code = target_code
                    detection_start_time = time.time()
            else:
                detection_start_time = None
                last_detected_code = None
        else:
            # Si no hay nada en camara, reseteamos el 'ultimo beeped' para que la proxima vez que entre algo suene
            last_beeped_code = None
            detection_start_time = None
            last_detected_code = None

        full_ui = draw_ui(frame, registered_items, highlighted_code, status_msg, progress)
        cv2.imshow('Lector Barcode Vision Expert', full_ui)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
