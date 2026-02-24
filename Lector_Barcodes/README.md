# LectorBarcodes - Barcode Vision Expert

Sistema avanzado de escaneo de códigos de barras con gestión de inventario persistente.

## Características
- **Interfaz Dividida**: Cámara a la izquierda y panel de control a la derecha.
- **Detección Inteligente**: Identificación instantánea de productos registrados.
- **Lista en Tiempo Real**: Los productos registrados aparecen arriba a la derecha y se resaltan al ser escaneados.
- **Registro de Nuevos Productos**: Si mantienes un código desconocido 1 segundo, el sistema te pedirá registrarlo abajo a la derecha.
- **Base de Datos**: Integración con SQLite para persistencia total.
- **Historial**: Logs automáticos en `ResultadosEscaneo/`.

## Requisitos
- Python 3.8+
- Cámara web conectada.

## Configuración de Sonidos
Para que el sistema emita sonidos, debes colocar tus archivos `.mp3` en la carpeta `assets/`:
1. **success.mp3**: Sonido que sonará al detectar un producto ya registrado.
2. **register.mp3**: Sonido que sonará al completar un registro nuevo.

*El sistema tiene un limitador de 1 segundo entre sonidos de detección para evitar ruidos molestos.*

## Instalación

1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   *Nota: En Windows, pyzbar requiere que las DLLs de Visual C++ estén instaladas.*

2. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

## Cómo conectar la cámara del PC
El script utiliza `cv2.VideoCapture(0)` por defecto.
- Si tienes varias cámaras, puedes cambiar el `0` por `1`, `2`, etc., en el archivo `app.py`.
- Asegúrate de que ninguna otra aplicación esté usando la cámara.

## Estructura de Archivos
- `app.py`: Lógica principal y visualización.
- `database.py`: Funciones de base de datos.
- `inventory.db`: Base de datos SQLite (se genera al iniciar).
- `ResultadosEscaneo/`: Carpeta con los logs de escaneos.
