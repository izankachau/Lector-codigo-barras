# GUÍA DE IMPLEMENTACIÓN: PROGRAMACIÓN EN SCL PARA SIEMENS

## 1. Introducción al entorno TIA Portal
Para programar en SCL, el entorno estándar de Siemens es **TIA Portal (Totally Integrated Automation)**. En esta guía, nos enfocaremos en la creación de bloques de código estructurado para procesos industriales.

## 2. Configuración del Bloque de Código
1.  Abrir el proyecto en TIA Portal.
2.  Navegar a "Program Blocks" -> "Add new block".
3.  Seleccionar "Function Block (FB)" o "Function (FC)".
4.  En el desplegable de **Language**, seleccionar **SCL**.

## 3. Estructura Básica del Código
Un programa en SCL se divide en:
-   **Declaración de variables**: En la parte superior (Interface), definimos Inputs, Outputs, InOut y Static.
-   **Lógica de control**: El cuerpo del programa donde escribimos las instrucciones.

### Ejemplo de sintaxis:
```scl
// Control de una bomba con consigna
IF "Input_Sensor" > #Temp_Max THEN
    "Bomba_Status" := TRUE;
    #Alarma := 1;
ELSE
    "Bomba_Status" := FALSE;
    #Alarma := 0;
END_IF;
```

## 4. Mejores Prácticas (Clean Code Industrial)
-   **Comentarios**: Utilizar `//` para explicar por qué se hace una acción, no qué hace la línea.
-   **Nomenclatura**: Usar PascalCase para variables globales y prefijo `#` para variables locales.
-   **Modularidad**: No crear bloques gigantes. Dividir la lógica en funciones pequeñas y específicas.

## 5. Depuración y Pruebas
-   **Monitorización**: Utilizar el botón de las gafas en TIA Portal para ver los valores en tiempo real.
-   **Simulación**: Usar **PLCSIM** para probar la lógica SCL sin necesidad de hardware real, asegurando que el flujo de datos es el correcto.

## 6. Conclusión
La programación en SCL permite crear sistemas industriales escalables y robustos. Seguir estas pautas asegura que el código sea comprensible por cualquier otro ingeniero en el futuro.
