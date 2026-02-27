# MANUAL DE USUARIO: SCL PRO ANALYZER v2.0

## 1. Descripción de la Solución
**SCL Pro Analyzer v2.0** es un entorno de desarrollo integrado (IDE) ligero diseñado para la creación, validación y gestión de programas en lenguaje **SCL (Siemens)** bajo la norma **IEC 61131-3**. La herramienta garantiza que el código escrito sea sintácticamente correcto antes de cargarlo en TIA Portal.

## 2. Instrucciones de Funcionamiento

### Fase de Inicio
- Ejecute el archivo `app.py`.
- Acceda a `http://localhost:5000` en su navegador.

### Gestión de la Librería Industrial (CRUD)
- **Cargar**: Haga clic en cualquier elemento de la lista de la derecha para cargar una plantilla profesional.
- **Guardar/Editar**: Pulse **"GUARDAR PLANTILLA"**. Si es una nueva, se abrirá un panel para definir sus metadatos (Nombre, Categoría, Descripción). Si ya existía, se actualizará el código en la base de datos.
- **Eliminar**: Use el botón `x` rojo para borrar plantillas obsoletas de la librería.
- **Nuevo**: Use **"LIMPIAR"** para resetear el editor.

### Análisis y Diagnóstico
- Escriba o pegue su código en el editor central.
- Pulse **"ANALIZAR CÓDIGO"**.
- El sistema devolverá:
  - **Ubicación**: Número de línea exacto.
  - **Descripción**: Qué error técnico se ha detectado (Ej: Falta de ';').
  - **Sugerencia**: La solución exacta para corregir el código bajo el estándar.

## 3. Normativas y Estándares
El software valida automáticamente los siguientes puntos de la norma IEC 61131-3:
1. Terminación de sentencias con `;`.
2. Cierre obligatorio de bloques (`END_IF`, `END_FOR`, etc.).
3. Palabras clave reservadas del estándar Siemens SCL.

## 4. Resolución de Problemas
- **Servidor no responde**: Verifique que tiene instalado Flask (`pip install flask`).
- **Error en base de datos**: Asegúrese de que el archivo `scl_library.db` tiene permisos de escritura.
