import asyncio
import threading
import os
import customtkinter as ctk
from asyncua import Client
from tkinter import messagebox

# --- CONFIGURACIÓN VISUAL FUTURISTA ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

class OPCUAClientApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OPC-UA CORE v1.0 - Izan Pons")
        self.geometry("900x650")

        # Variables de estado
        self.client = None
        self.is_connected = False
        self.server_url = "opc.tcp://localhost:4842/freeopcua/server/"

        # UI Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- BARRA LATERAL (CYBER) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0A0B10")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="OPC-UA\nCORE", font=ctk.CTkFont(size=26, weight="bold", family="Orbitron"))
        self.logo.grid(row=0, column=0, padx=20, pady=(40, 40))

        self.conn_btn = ctk.CTkButton(self.sidebar, text="INIT LINK", 
                                     fg_color="#00A8FF", hover_color="#007AFF",
                                     font=ctk.CTkFont(weight="bold"),
                                     command=self.toggle_connection)
        self.conn_btn.grid(row=1, column=0, padx=20, pady=10)

        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, padx=20, pady=20)
        
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", text_color="#FF3B30", font=ctk.CTkFont(size=20))
        self.status_dot.grid(row=0, column=0, padx=5)
        
        self.status_text = ctk.CTkLabel(self.status_frame, text="DISCONNECTED", font=ctk.CTkFont(size=12, weight="bold"))
        self.status_text.grid(row=0, column=1)

        self.footer_label = ctk.CTkLabel(self.sidebar, text="SYSTEM v1.0\nIZAN PONS 2026", 
                                        font=ctk.CTkFont(size=10), text_color="#555555")
        self.footer_label.grid(row=4, column=0, pady=(200, 20))

        # --- ÁREA PRINCIPAL (GLASSMORPHISM STYLE) ---
        self.main = ctk.CTkFrame(self, fg_color="#101219")
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main.grid_columnconfigure((0, 1), weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        self.header = ctk.CTkLabel(self.main, text="INDUSTRIAL MONITORING DASHBOARD", 
                                  font=ctk.CTkFont(size=18, weight="bold", letter_spacing=2))
        self.header.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Widgets de datos con estilo neón
        self.create_data_widget("TEMPERATURE", "temp_val", 1, 0, "°C", "#00A8FF")
        self.create_data_widget("PRESSURE", "pres_val", 1, 1, "BAR", "#00FFCC")
        self.create_data_widget("UNIT COUNTER", "cont_val", 2, 0, "UDS", "#FFD700")
        self.create_data_widget("SYSTEM STATE", "stat_val", 2, 1, "LOGICTRAN", "#FF3B30")

        self.log_box = ctk.CTkTextbox(self.main, height=120, fg_color="#050608", 
                                     border_color="#1A1C23", border_width=1,
                                     font=ctk.CTkFont(family="Consolas", size=11), text_color="#00FFCC")
        self.log_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(20, 0))
        self.log_box.insert("end", "> INITIALIZING SYSTEM CORE...\n> READY FOR UPLINK.\n")

    def create_data_widget(self, label_text, var_name, r, c, unit, neon_color):
        frame = ctk.CTkFrame(self.main, fg_color="#161922", border_color="#232732", border_width=1)
        frame.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
        
        lbl = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=11, weight="bold"), text_color="#888888")
        lbl.pack(pady=(15, 0))
        
        val_lbl = ctk.CTkLabel(frame, text="--", font=ctk.CTkFont(size=42, weight="bold"), text_color=neon_color)
        val_lbl.pack(pady=10)
        
        unit_lbl = ctk.CTkLabel(frame, text=unit, font=ctk.CTkFont(size=10, weight="bold"), text_color="#444444")
        unit_lbl.pack(pady=(0, 15))
        
        setattr(self, var_name, val_lbl)

    def toggle_connection(self):
        if not self.is_connected:
            self.log_box.insert("end", "> ATTEMPTING UPLINK TO SERVER...\n")
            threading.Thread(target=self.run_async_client, daemon=True).start()
        else:
            self.is_connected = False

    def run_async_client(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_to_server())

    async def connect_to_server(self):
        try:
            async with Client(url=self.server_url) as client:
                self.client = client
                self.is_connected = True
                self.after(0, lambda: self.status_dot.configure(text_color="#00FFCC"))
                self.after(0, lambda: self.status_text.configure(text="SECURE LINK: ACTIVE"))
                self.after(0, lambda: self.conn_btn.configure(text="TERMINATE", fg_color="#FF3B30"))
                self.after(0, lambda: self.log_box.insert("end", f"> CONNECTION STABLISHED: {self.server_url}\n"))

                idx = 2
                node_temp = await client.nodes.root.get_child(["0:Objects", f"{idx}:Maquina_Produccion", f"{idx}:Temperatura"])
                node_pres = await client.nodes.root.get_child(["0:Objects", f"{idx}:Maquina_Produccion", f"{idx}:Presion"])
                node_cont = await client.nodes.root.get_child(["0:Objects", f"{idx}:Maquina_Produccion", f"{idx}:Contador_Piezas"])
                node_stat = await client.nodes.root.get_child(["0:Objects", f"{idx}:Maquina_Produccion", f"{idx}:Estado_Marcha"])

                while self.is_connected:
                    v_temp = await node_temp.read_value()
                    v_pres = await node_pres.read_value()
                    v_cont = await node_cont.read_value()
                    v_stat = await node_stat.read_value()

                    self.after(0, lambda t=v_temp: self.temp_val.configure(text=f"{t:.1f}"))
                    self.after(0, lambda p=v_pres: self.pres_val.configure(text=f"{p:.2f}"))
                    self.after(0, lambda c=v_cont: self.cont_val.configure(text=str(c)))
                    self.after(0, lambda s=v_stat: self.stat_val.configure(text="ACTIVE" if s else "HALTHED", text_color="#00FFCC" if s else "#FF3B30"))
                    
                    await asyncio.sleep(0.5)

        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: messagebox.showerror("LINK FAILURE", f"System could not establish connection:\n{error_msg}"))
        finally:
            self.is_connected = False
            self.after(0, lambda: self.status_dot.configure(text_color="#FF3B30"))
            self.after(0, lambda: self.status_text.configure(text="DISCONNECTED"))
            self.after(0, lambda: self.conn_btn.configure(text="INIT LINK", fg_color="#00A8FF"))
            self.after(0, lambda: self.log_box.insert("end", "> CONNECTION TERMINATED.\n"))

if __name__ == "__main__":
    app = OPCUAClientApp()
    app.mainloop()
