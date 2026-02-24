import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from database import init_db, get_item, add_item, update_item_name, update_item_price, delete_item, DB_PATH
import sqlite3
import threading
from playsound import playsound

# Configuración de sonidos
ASSETS_DIR = "assets"
SOUND_SUCCESS = os.path.join(ASSETS_DIR, "success.mp3")
SOUND_REGISTER = os.path.join(ASSETS_DIR, "register.mp3")
SOUND_CASH = os.path.join(ASSETS_DIR, "cash.mp3")

import pyttsx3

# Configuración de voz e IA
engine = pyttsx3.init()
engine.setProperty('rate', 150) # Velocidad de voz

# Variables globales
last_beeped_code = None
SOUND_COOLDOWN = 1.0
shopping_list = [] # {"name": str, "code": str, "units": int, "price": float}
sales_stats = {} 
search_query = ""

# Temas (Neon, Vampire, Matrix)
current_theme = 0
themes = [
    {"bg": (35, 35, 35), "panel": (50, 60, 80), "accent": (0, 255, 100), "name": "NEO-CIAN"},
    {"bg": (10, 10, 25), "panel": (30, 0, 50), "accent": (0, 100, 255), "name": "CYBER-NIGHT"},
    {"bg": (5, 20, 5), "panel": (0, 40, 0), "accent": (0, 255, 0), "name": "MATRIX"}
]

# Lógica de detección estable
stable_code = None
stable_start_time = None
REQUIRED_STABLE_TIME = 1.0 

# Efecto Secreto 67
secret_67_start = 0
show_secret_67 = False

# Scroll e Interacción
scroll_offset = 0
btn_exit_rect_global = [0, 0, 0, 0]
btn_reset_rect_global = [0, 0, 0, 0]
btn_print_rect_global = [0, 0, 0, 0]
btn_search_rect = [0, 0, 0, 0]

item_display_rects = []
mouse_pos = (0, 0)

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

def play_audio(file_path):
    if os.path.exists(file_path):
        threading.Thread(target=playsound, args=(file_path,), daemon=True).start()

def get_all_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, price FROM inventory ORDER BY name ASC")
    items = cursor.fetchall()
    conn.close()
    return items

def draw_futuristic_text(canvas, text, pos, font_scale, color, thickness=1):
    cv2.putText(canvas, text, (pos[0]+1, pos[1]+1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (10, 10, 10), thickness+1)
    cv2.putText(canvas, text, pos, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

def draw_styled_panel(canvas, x1, y1, x2, y2, title, base_color):
    cv2.rectangle(canvas, (x1, y1), (x2, y2), base_color, -1)
    cv2.rectangle(canvas, (x1, y1), (x2, y2), (200, 200, 200), 1)
    cv2.rectangle(canvas, (x1, y1), (x2, y1+30), (20, 20, 20), -1)
    draw_futuristic_text(canvas, title.upper(), (x1 + 10, y1 + 22), 0.45, (255, 255, 255), 1)

def draw_ui(frame, registered_items, highlighted_code=None, status_msg="SISTEMA ACTIVO", progress=0, barcode_rect=None):
    global btn_exit_rect_global, btn_reset_rect_global, btn_print_rect_global, btn_search_rect, item_display_rects, scroll_offset, mouse_pos, show_secret_67, secret_67_start, current_theme
    theme = themes[current_theme]
    h, w, _ = frame.shape
    ui_width = int(w * 2.1)
    canvas = np.zeros((h, ui_width, 3), dtype=np.uint8)
    canvas.fill(theme["bg"][0]) 

    # Filtrar por búsqueda
    filtered_items = [it for it in registered_items if search_query.lower() in it[1].lower()]

    # Cámara
    canvas[0:h, 0:w] = frame
    if barcode_rect:
        (rx, ry, rw, rh) = barcode_rect
        cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), theme["accent"], 2)

    panel_x = w + 15
    panel_w = ui_width - panel_x - 15
    
    # --- PANEL BUSQUEDA Y TEMA ---
    cv2.rectangle(canvas, (panel_x, 10), (ui_width - 15, 45), (40, 40, 40), -1)
    draw_futuristic_text(canvas, f"TEMA: {theme['name']} (Pulse T)", (panel_x+10, 30), 0.4, (200, 200, 200), 1)
    btn_search_rect = [panel_x + panel_w//2, 10, ui_width - 15, 45]
    cv2.rectangle(canvas, (btn_search_rect[0], 10), (btn_search_rect[2], 45), (60, 60, 60), -1)
    draw_futuristic_text(canvas, f"BUSCAR: {search_query[:10]}", (btn_search_rect[0]+10, 30), 0.4, (0, 255, 255), 1)

    # --- INVENTARIO ---
    inv_y1, inv_y2 = 55, h // 2 - 20
    draw_styled_panel(canvas, panel_x, inv_y1, ui_width - 15, inv_y2, "LISTADO PRODUCTOS", theme["panel"])
    
    y_start = inv_y1 + 45
    item_h = 32
    max_visible = (inv_y2 - y_start) // item_h
    item_display_rects = []
    
    if scroll_offset < 0: scroll_offset = 0
    if len(filtered_items) > max_visible:
        if scroll_offset > len(filtered_items) - max_visible: scroll_offset = len(filtered_items) - max_visible
    else: scroll_offset = 0

    visible_items = filtered_items[scroll_offset : scroll_offset + max_visible]
    for i, (code, name, price) in enumerate(visible_items):
        iy = y_start + i * item_h
        rect = (panel_x + 5, iy, ui_width - 20, iy + item_h - 4)
        item_display_rects.append((rect, code))
        is_hover = rect[0] <= mouse_pos[0] <= rect[2] and rect[1] <= mouse_pos[1] <= rect[3]
        col = (60, 60, 80)
        txt_c = (255, 255, 255)
        if code == highlighted_code: col = theme["accent"]; txt_c = (0, 0, 0)
        elif is_hover: col = (100, 100, 130)
        cv2.rectangle(canvas, (rect[0], rect[1]), (rect[2], rect[3]), col, -1)
        draw_futuristic_text(canvas, name[:35], (rect[0]+10, rect[1]+20), 0.4, txt_c, 1)
        draw_futuristic_text(canvas, f"{price:.2f}E", (rect[2]-60, rect[1]+20), 0.4, (0, 255, 255), 1)

    # --- CARRITO (Anterioremente Cesta de la Compra) ---
    shop_y1, shop_y2 = h // 2 + 10, h - 130
    draw_styled_panel(canvas, panel_x, shop_y1, ui_width - 15, shop_y2, "LISTA DE LA COMPRA", theme["panel"])
    ys = shop_y1 + 50
    for item in shopping_list[-4:]:
        draw_futuristic_text(canvas, f"- {item['units']}x {item['name'][:20]} = {item['units']*item['price']:.2f}E", (panel_x+10, ys), 0.4, (255, 255, 255), 1)
        ys += 25

    # --- BOTONES ---
    bw = (panel_w // 3) - 8; bh = 40; by = h - 60
    for i, (lbl, clr) in enumerate([("REINICIAR", (100, 50, 50)), ("TICKET", (50, 100, 50)), ("SALIR", (80, 80, 80))]):
        bx = panel_x + i * (bw + 10)
        brect = [bx, by, bx+bw, by+bh]
        b_hover = brect[0] <= mouse_pos[0] <= brect[2] and brect[1] <= mouse_pos[1] <= brect[3]
        cv2.rectangle(canvas, (bx, by), (bx+bw, by+bh), tuple(min(255, c+40) for c in clr) if b_hover else clr, -1)
        draw_futuristic_text(canvas, lbl, (bx+12, by+27), 0.45, (255,255,255), 1)
        if i == 0: btn_reset_rect_global = brect
        elif i == 1: btn_print_rect_global = brect
        else: btn_exit_rect_global = brect

    # Secreto 67
    if show_secret_67:
        if time.time() - secret_67_start > 3.0: show_secret_67 = False
        else:
            fc = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
            cv2.putText(canvas, "67", (w//2-80, h//2+50), cv2.FONT_HERSHEY_BOLD, 8.0, fc, 15)

    if progress > 0:
        cv2.rectangle(canvas, (10, h-15), (w-10, h-5), (40, 40, 40), -1)
        cv2.rectangle(canvas, (10, h-15), (10+int((w-20)*progress/100), h-5), theme["accent"], -1)

    draw_futuristic_text(canvas, f"> {status_msg}", (panel_x+5, h-100), 0.45, theme["accent"], 1)
    return canvas

def ask_user(title, prompt, is_float=False):
    root = tk.Tk(); root.withdraw()
    result = simpledialog.askstring(title, prompt)
    root.destroy()
    if is_float and result:
        try: return float(result.replace(',', '.'))
        except: return 0.0
    return result

def ask_integer(title, prompt):
    root = tk.Tk(); root.withdraw()
    result = simpledialog.askinteger(title, prompt)
    root.destroy()
    return result

def show_ticket():
    global shopping_list, sales_stats, show_secret_67, secret_67_start
    if not shopping_list:
        messagebox.showwarning("Vacio", "No hay productos.")
        return
    play_audio(SOUND_CASH)
    total = sum(item['units'] * item['price'] for item in shopping_list)
    total_iva = total * 1.21
    
    ticket_text = f"TICKET DE COMPRA\n{'-'*30}\n"
    for item in shopping_list:
        ticket_text += f"{item['units']}x {item['name'][:20]} {item['units']*item['price']:>6.2f}E\n"
        sales_stats[item['name']] = sales_stats.get(item['name'], 0) + item['units']
        
    ticket_text += f"{'-'*30}\nTOTAL IVA INCL: {total_iva:.2f}E\n\nATENDIDO POR MONICIUS JUNIOR"
    
    speak(f"El total es de {total_iva:.2f} euros. Gracias por su compra.")
    
    total_items = sum(it['units'] for it in shopping_list)
    if total_items == 67: show_secret_67 = True; secret_67_start = time.time()
    
    root = tk.Tk(); root.title("Ticket")
    tk.Label(root, text=ticket_text, font=("Consolas", 11), justify=tk.LEFT, padx=20, pady=20).pack()
    def end(): global shopping_list; shopping_list=[]; root.destroy()
    tk.Button(root, text="LISTO", command=end, bg="green", fg="white").pack(pady=10)
    root.mainloop()

# Flags para control desde callback
force_exit = False
refresh_needed = False

def handle_right_click(code):
    global refresh_needed
    item = get_item(code)
    if not item: return
    name, _, price = item
    root = tk.Tk(); root.title("ADMIN"); root.geometry("280x250")
    
    def edit(m):
        if m == "n":
            nn = simpledialog.askstring("Nombre", "Nuevo nombre:")
            if nn: update_item_name(code, nn)
        elif m == "p":
            np = simpledialog.askfloat("Precio", "Nuevo precio:")
            if np: update_item_price(code, np)
        elif m == "d":
            if messagebox.askyesno("Borrar", "¿Eliminar producto?"): delete_item(code)
        root.destroy()

    tk.Label(root, text=f"GESTIÓN: {name[:20]}", font=("Bold", 11)).pack(pady=10)
    tk.Button(root, text="Editar Nombre", command=lambda: edit("n"), width=20, pady=5).pack(pady=2)
    tk.Button(root, text="Editar Precio", command=lambda: edit("p"), width=20, pady=5).pack(pady=2)
    tk.Button(root, text="Eliminar Producto", command=lambda: edit("d"), bg="#D32F2F", fg="white", width=20, pady=5).pack(pady=15)
    tk.Button(root, text="Cancelar", command=root.destroy, width=20).pack()
    
    root.mainloop()
    refresh_needed = True

def on_mouse(event, x, y, flags, param):
    global shopping_list, force_exit, refresh_needed, scroll_offset, mouse_pos, search_query
    mouse_pos = (x, y)
    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0: scroll_offset -= 1
        else: scroll_offset += 1
    if event == cv2.EVENT_LBUTTONDOWN:
        if btn_search_rect[0] <= x <= btn_search_rect[2] and btn_search_rect[1] <= y <= btn_search_rect[3]:
            search_query = ask_user("Buscar", "Nombre del producto:") or ""
        elif btn_exit_rect_global[0] <= x <= btn_exit_rect_global[2] and btn_exit_rect_global[1] <= y <= btn_exit_rect_global[3]:
            force_exit = True
        elif btn_reset_rect_global[0] <= x <= btn_reset_rect_global[2] and btn_reset_rect_global[1] <= y <= btn_reset_rect_global[3]:
            shopping_list = []; messagebox.showinfo("Reset", "Limpio.")
        elif btn_print_rect_global[0] <= x <= btn_print_rect_global[2] and btn_print_rect_global[1] <= y <= btn_print_rect_global[3]:
            show_ticket()
    elif event == cv2.EVENT_RBUTTONDOWN:
        for r, c in item_display_rects:
            if r[0] <= x <= r[2] and r[1] <= y <= r[3]: handle_right_click(c); break

def main():
    global last_beeped_code, shopping_list, force_exit, refresh_needed, stable_code, stable_start_time, show_secret_67, secret_67_start, search_query, current_theme
    
    # Configuración inicial de archivos (movido aquí para asegurar persistencia)
    # SCAN_RESULTS_DIR = "ResultadosEscaneo" # No usado en este snippet
    if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)
    init_db()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return

    cv2.namedWindow('Lector Barcode Vision Expert', cv2.WINDOW_NORMAL) # Habilitar ajuste de tamaño
    cv2.setMouseCallback('Lector Barcode Vision Expert', on_mouse)

    db_cache = {}
    def refresh():
        items = get_all_items()
        db_cache.clear()
        for c, n, p in items: db_cache[c] = (n, p)
        return items

    reg_items = refresh()

    while True:
        if force_exit: break
        if refresh_needed: reg_items = refresh(); refresh_needed = False
            
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = decode(gray)
        
        status = "LISTO"; highlighted = None; prog = 0; brect = None
        
        if barcodes:
            # Seleccionamos el primer barcode detectado
            b = barcodes[0]
            current = b.data.decode('utf-8')
            brect = b.rect # Para el recuadro verde
            
            # Gestión de estabilidad de 1 segundo
            if current == stable_code:
                if stable_start_time is None: stable_start_time = time.time()
                elapsed = time.time() - stable_start_time
                prog = min(100, int(elapsed * 100))
                status = f"ESCANEANDO {prog}%"
                
                # SI PASA EL SEGUNDO
                if elapsed >= REQUIRED_STABLE_TIME:
                    data = db_cache.get(current)
                    if data:
                        n, p = data
                        highlighted = current
                        status = f"VISTO: {n}"
                        
                        # Suena el primer sonido (Success) al completar el segundo
                        if current != last_beeped_code:
                            play_audio(SOUND_SUCCESS)
                            last_beeped_code = current
                            
                            # VOZ
                            speak(f"{n}, {p} euros")
                            
                            # Preguntar unidades
                            u = ask_integer("Ventas", f"¿Unidades de {n}?")
                            if u and u > 0:
                                if u == 67: show_secret_67 = True; secret_67_start = time.time()
                                shopping_list.append({"name": n, "code": current, "units": u, "price": p})
                    else:
                        # Si es nuevo, permitir registrar
                        status = "NUEVO"
                        # Suena sonido de éxito aunque sea nuevo para indicar que se leyó bien
                        if current != last_beeped_code:
                            play_audio(SOUND_SUCCESS)
                            last_beeped_code = current

                        if messagebox.askyesno("Nuevo", "¿Registrar?"):
                            n = ask_user("Nombre", "Nombre:")
                            if n:
                                p = ask_user("Precio", "Precio:", is_float=True)
                                add_item(current, n, p)
                                play_audio(SOUND_REGISTER) # Segundo sonido al registrar
                                reg_items = refresh()
                    
                    # Reset para que no se ejecute en bucle infinito sobre el mismo código sostenido
                    # O podrías resetear stable_start_time a algo muy antiguo si quieres re-lectura
                    stable_start_time = time.time() - 10 
            else:
                stable_code = current
                stable_start_time = time.time()
        else:
            stable_code = None
            stable_start_time = None
            last_beeped_code = None

        ui = draw_ui(frame, reg_items, highlighted, status, prog, brect)
        cv2.imshow('Lector Barcode Vision Expert', ui)
        key = cv2.waitKey(1)
        if key == ord('q'): break
        elif key == ord('s'): # Tecla 's' para activar la búsqueda
            search_query = ask_user("Buscar", "Introduce texto a buscar:") or ""

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
