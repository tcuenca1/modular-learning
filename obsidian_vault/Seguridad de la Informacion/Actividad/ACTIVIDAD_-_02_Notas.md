---
materia: Seguridad de la Informacion
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [seguridad_de_la_informacion, actividad, ingesta_ia]
---

# [[Seguridad de la Informacion]]: Práctica de Laboratorio: Mini-Simulacro Técnico de Seguridad de la Información

**Estudiantes:** [ESTUDIANTE], [ESTUDIANTE]

Esta práctica de laboratorio tiene como objetivo que los estudiantes comprendan los pilares de la [[Seguridad de la Información]] (Confidencialidad, Integridad y Disponibilidad) mediante ejercicios prácticos utilizando [[PowerShell]] en [[Windows]].

---

## Actividad 1: Codificar y decodificar mensajes (Confidencialidad)

* **Objetivo:** demostrar cómo un mensaje legible se convierte en ilegible y viceversa.

### Pasos:
1. Abrir [[PowerShell]].
2. Ejecutar el siguiente script para codificar un mensaje:

```powershell
$Text = "La clase de seguridad es hoy"
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)
$Encoded = [Convert]::ToBase64String($Bytes)
$Encoded
```

3. Para decodificar el mensaje, ejecutar:

```powershell
$Decoded = [System.Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Encoded))
$Decoded
```

### Resultados registrados:

| Concepto | Resultado |
| :--- | :--- |
| **Texto original** | La clase de seguridad es hoy |
| **Texto codificado** | `TABhACAAYwBsAGEAcwBlACAAZABlACAAcwBlAGcAdQByAGkAZABhAGQAIABlAHMAIABoAG8AeQA=` |
| **Texto decodificado** | La clase de seguridad es hoy |

---

## Actividad 2: Hash de archivo y comparación (Integridad)

* **Objetivo:** comprobar cómo cambia el [[Hash]] si alteramos un archivo.

### Pasos:
1. Crear un archivo `mensaje.txt` con el texto: `'Seguridad de la Información'`.
2. En [[PowerShell]] ejecutar:

```powershell
Get-FileHash mensaje.txt -Algorithm SHA256
```

3. Modificar el archivo agregando un punto al final.
4. Volver a calcular el [[Hash]] con el mismo comando.

### Resultados registrados:

| Concepto | Resultado |
| :--- | :--- |
| **Hash original** | `4EB9C7987E4F453EDE7B00A432868E806C6C496B27732B7D625D41E57B927B4C` |
| **Hash modificado** | `F6BB3A866D66ED9C458C542ADCF2CB18E9A065D63135733658B232F4171CBB02` |

### ¿Qué es un [[Hash]]?
Es un algoritmo matemático que transforma cualquier bloque de datos en una cadena de caracteres alfanuméricos de longitud fija. Actúa como una huella digital única de ese archivo en ese momento exacto.

### ¿Para qué sirve un [[Hash]]?
Sirve para garantizar y verificar la **[[Integridad]]** de la información. Permite comprobar si un archivo ha sido modificado, corrompido o manipulado por terceros; si el [[Hash]] de un archivo descargado coincide con el original, significa que está intacto.

---

## Actividad 3: Simulación de servicio no disponible (Disponibilidad)

* **Objetivo:** comprobar qué ocurre cuando un servicio no está disponible.

### Pasos:
1. Ejecutar en [[PowerShell]]:

```powershell
ping noexiste1234.com
```

2. Luego comparar con un sitio real:

```powershell
ping google.com
```

### Observaciones registradas:

| Acción | Resultado |
| :--- | :--- |
| **Resultado al hacer ping a `noexiste1234.com`** | “La solicitud de ping no pudo encontrar el host noexiste1234.com. Compruebe el nombre y vuelva a intentarlo.” |
| **Resultado al hacer ping a `google.com`** | Haciendo ping a `google.com` [172.217.30.174] con 32 bytes de datos:<br>Respuesta desde 172.217.30.174: bytes=32 tiempo=81ms TTL=251<br>Respuesta desde 172.217.30.174: bytes=32 tiempo=82ms TTL=251<br>Respuesta desde 172.217.30.174: bytes=32 tiempo=84ms TTL=251<br>Respuesta desde 172.217.30.174: bytes=32 tiempo=87ms TTL=251<br><br>**Estadísticas de ping para 172.217.30.174:**<br>Paquetes: enviados = 4, recibidos = 4, perdidos = 0 (0% perdidos)<br>Tiempos aproximados de ida y vuelta en milisegundos: Mínimo = 81ms, Máximo = 87ms, Media = 83ms |

### ¿La redundancia ayuda a la [[Disponibilidad]]? SI/NO. Justifique
**Sí**, la redundancia consiste en tener sistemas, hardware o enlaces de red duplicados. Si el servidor o la conexión principal fallan, el sistema redundante toma el control automáticamente. Esto asegura que el sistema siga operando y la información esté disponible para los usuarios sin interrupciones.

---

## Resumen y Conclusiones

* **[[Hash]] cambiado** $\rightarrow$ garantiza la [[Integridad]].
* **Servicio caído** $\rightarrow$ afecta la [[Disponibilidad]].

**Conclusiones del estudiante:** Con la resolución de las tres actividades se han puesto en práctica los tres pilares de la seguridad de la información (CID). Por el lado de la confidencialidad, se logró ocultar los datos mediante codificación, haciendo uso de hashes; por la integridad, se aseguró calculando y comparando hashes, permitiendo detectar alteraciones en un archivo; por último, la disponibilidad se verifica con pruebas de conectividad de red recordando implementar redundancia para evitar dificultades de acceso al sistema.

---

## ANEXOS: Anexar las capturas de pantalla de las prácticas

### Actividad 1
> **Captura de código detectada:** Ventana de consola de [[PowerShell]] ejecutando las sentencias de codificación Base64 en [[Windows]], mostrando el texto original y la variable `$Encoded` resultante de la conversión.

### Actividad 2
> **Captura de código detectada:** Ventanas de la consola de [[PowerShell]] ejecutando el comando `Get-FileHash mensaje.txt -Algorithm SHA256` antes y después de modificar el archivo, mostrando el cambio en la cadena [[Hash]] SHA256 correspondiente.

### Actividad 3
> **Captura de consola detectada:** Ejecución del comando `ping noexiste1234.com` retornando error de resolución de host, seguida de la traza de ejecución del comando `ping google.com` devolviendo estadísticas de tiempo de respuesta e intercambio de paquetes exitoso (0% perdidos).