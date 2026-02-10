# Lector de Códigos de Barras - Vision Expert

Este es un sistema avanzado de escaneo de códigos de barras desarrollado en Python, diseñado para la gestión de inventario en tiempo real con una interfaz visual intuitiva.

**Autor:** Izan Pons
**GitHub:** [izankachau](https://github.com/izankachau)

## 🚀 Descripción
El proyecto utiliza visión artificial para detectar códigos de barras a través de la webcam. Permite registrar nuevos productos, gestionar una base de datos local y emitir notificaciones sonoras. Es ideal para pequeños comercios o control de stock personal.

### Características principales
- **Interfaz Dividida**: Cámara en tiempo real y panel de control lateral.
- **Detección Inteligente**: Identificación instantánea con resaltado visual.
- **Registro Dinámico**: Si un código no existe, el sistema solicita su registro tras 1 segundo de detección.
- **Persistencia de Datos**: Base de datos SQLite integrada.
- **Feedback Auditivo**: Sonidos personalizados para escaneos exitosos y registros.

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu ordenador:

### 1. Clonar el repositorio
```bash
git clone https://github.com/izankachau/Lector-Codigo-Barras.git
cd Lector-Codigo-Barras
```

### 2. Crear un entorno virtual (Recomendado)
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
*Nota: En Windows, `pyzbar` requiere tener instaladas las [Visual C++ Redistributable Packages](https://www.microsoft.com/en-us/download/details.aspx?id=48145).*

### 4. Ejecutar la aplicación
```bash
python app.py
```

---

## 📂 Estructura del Proyecto
- `app.py`: El corazón del sistema (interfaz y lógica de visión).
- `database.py`: Gestión de la base de datos SQLite.
- `assets/`: Archivos de audio (`success.mp3` y `register.mp3`).
- `ResultadosEscaneo/`: Histórico de escaneos realizados.

---

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

