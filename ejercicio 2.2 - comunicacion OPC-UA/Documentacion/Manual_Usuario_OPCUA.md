# MANUAL DE USUARIO: MONITOR INDUSTRIAL OPC-UA CORE v1.0

## 1. Introducción
Este software es un ecosistema completo de comunicación industrial optimizado para **Python 3.13**, garantizando estabilidad y rendimiento en entornos de automatización modernos.

## 2. Requisitos de Instalación
Para que el sistema funcione correctamente, debes instalar las librerías utilizando el lanzador de Python 3.13:
```bash
py -3.13 -m pip install asyncua customtkinter
```

## 3. Guía de Ejecución Rápida
Debido a la compatibilidad necesaria con versiones específicas de Python, sigue este orden exacto desde tu terminal CMD:

### Paso 1: Activar el Servidor (Simulador Industrial)
```bash
cd "Examen_Informatica/ejercicio 2.2 - comunicacion OPC-UA/Programa_OPCUA"
py -3.13 server_opcua.py
```
*Este proceso debe mantenerse abierto para que el cliente pueda conectarse.*

### Paso 2: Ejecutar el Dashboard (Interfaz Futurista)
Abre otra terminal y ejecuta:
```bash
cd "Examen_Informatica/ejercicio 2.2 - comunicacion OPC-UA/Programa_OPCUA"
py -3.13 client_opcua.py
```

## 4. Uso de la Interfaz Futurista (Dashboard)
- **INIT LINK**: Presiona este botón para establecer una conexión segura con la máquina.
- **Visualización Neón**: Los datos de Temperatura (Azul), Presión (Cian) y Contador (Oro) se actualizan dinámicamente.
- **Terminal de Log**: Situada en la parte inferior, registra cada evento de la conexión en tiempo real.
- **Estado del Enlace**: Un indicador visual (rojo/verde) muestra si la comunicación está activa o interrumpida.

## 5. Datos Técnicos
- **Endpoint URL**: `opc.tcp://localhost:4842/freeopcua/server/`
- **Puerto**: 4842 (Optimizado para evitar bloqueos de red).
- **Entorno**: Compatible con sistemas operativos Windows en arquitectura x64.
