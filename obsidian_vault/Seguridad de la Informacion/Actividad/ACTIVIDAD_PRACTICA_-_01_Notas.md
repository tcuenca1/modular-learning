---
materia: Seguridad de la Informacion
tipo: actividad
fecha_procesamiento: 2026-10-01
tags: [seguridad_de_la_informacion, actividad, ingesta_ia]
---

# [[Seguridad de la Informacion]]: Práctica de Laboratorio: Mini-Simulacro Técnico de Seguridad de la Información

**Estudiantes:** [ESTUDIANTE], [ESTUDIANTE]

Esta práctica de laboratorio tiene como objetivo que los estudiantes comprendan los pilares de la [[Seguridad de la Informacion]] (**Confidencialidad, Integridad y Disponibilidad**) mediante ejercicios prácticos utilizando [[PowerShell]] en [[Windows]].

---

## Actividad 1: Codificar y decodificar mensajes (Confidencialidad)

* **Objetivo:** Demostrar cómo un mensaje legible se convierte en ilegible y viceversa.

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

### Registro de resultados:
* **Texto original:** La clase de seguridad es hoy
* **Texto codificado:** `TABhACAAYwBsAGEAcwBlACAAZABlACAAcwBlAGcAdQByAGkAZABhAGQAIABlAHMAIABoAG8AeQA=`
* **Texto decodificado:** La clase de seguridad es hoy

> **Captura de pantalla detectada (Actividad 1):** 
> Consola de [[PowerShell]] mostrando la ejecución de los comandos para asignar la variable `$Text`, convertirla a bytes [[Unicode]], codificarla en [[Base64]] y posteriormente decodificarla exitosamente mostrando el texto original en pantalla.

---

## Actividad 2: Hash de archivo y comparación (Integridad)

* **Objetivo:** Comprobar cómo cambia el [[Hash]] si alteramos un archivo.

### Pasos:
1. Crear un archivo `mensaje.txt` con el texto: `'Seguridad de la Información'`.
2. En [[PowerShell]] ejecutar:
   ```powershell
   Get-FileHash mensaje.txt -Algorithm SHA256
   ```
3. Modificar el archivo agregando un punto al final.
4. Volver a calcular el hash con el mismo comando.

### Registro de resultados:
* **Hash original:** `4EB9C7987E4F453EDE7B00A432868E806C6C496B27732B7D625D41E57B927B4C`
* **Hash modificado:** `F6BB3A866D66ED9C458C542ADCF2CB18E9A065D63135733658B232F4171CBB02`

---

### ¿Qué es un [[Hash]]?
Es un algoritmo matemático que transforma cualquier bloque de datos en una cadena de caracteres alfanuméricos de longitud fija. Actúa como una huella digital única de ese archivo en ese momento exacto.

### ¿Para qué sirve un [[Hash]]?
Sirve para garantizar y verificar la **integridad** de la información. Permite comprobar si un archivo ha sido modificado, corrompido o manipulado por terceros; si el hash de un archivo descargado coincide con el original, significa que está intacto.

> **Captura de pantalla detectada (Actividad 2):** 
> Ventana de [[PowerShell]] ejecutando el cmdlet `Get-FileHash` utilizando el algoritmo [[SHA256]] sobre el archivo `mensaje.txt`, evidenciando el cambio del valor hash tras la modificación del contenido.

---

## Actividad 3: Simulación de servicio no disponible (Disponibilidad)

* **Objetivo:** Comprobar qué ocurre cuando un servicio no está disponible.

### Pasos:
1. Ejecutar en [[PowerShell]]:
   ```powershell
   ping noexiste1234.com
   ```
2. Luego comparar con un sitio real:
   ```powershell
   ping google.com
   ```

### Registro de observaciones:
* **Resultado al hacer ping a `noexiste1234.com`:** 
  > *“La solicitud de ping no pudo encontrar el host noexiste1234.com. Compruebe el nombre y vuelva a intentarlo.”*
* **Resultado al hacer ping a `google.com`:** 
  > *Haciendo ping a google.com [172.217.30.174] con 32 bytes de datos:*
  > *Respuesta desde 172.217.30.174: bytes=32 tiempo=81ms TTL=251*
  > *Estadísticas de ping para 172.217.30.174: Paquetes: enviados = 4, recibidos = 4, perdidos = 0 (0% perdidos)*

---

### ¿La redundancia ayuda a la disponibilidad? **SI/NO**. Justifique
**Sí**, la redundancia consiste en tener sistemas, hardware o enlaces de red duplicados. Si el servidor o la conexión principal fallan, el sistema redundante toma el control automáticamente. Esto asegura que el sistema siga operando y la información esté disponible para los usuarios sin interrupciones.

> **Captura de pantalla detectada (Actividad 3):** 
> Consola de [[PowerShell]] reflejando el error de resolución de DNS al realizar el comando `ping` a un dominio inexistente, y el funcionamiento correcto al hacer ping al servidor con dirección IP `172.217.30.174` (google.com) junto con sus estadísticas de red.

---

## Resumen y Conclusiones
* **Hash cambiado** $\rightarrow$ Garantiza la **Integridad**.
* **Servicio caído** $\rightarrow$ Afecta la **Disponibilidad**.

**Conclusiones del estudiante:** 
Con la resolución de las tres actividades se han puesto en práctica los tres pilares de la seguridad de la información (CID). Por el lado de la **confidencialidad**, se logró ocultar los datos mediante codificación, haciendo uso de hashes; por la **integridad**, se aseguró calculando y comparando hashes, permitiendo detectar alteraciones en un archivo; por último, la **disponibilidad** se verifica con pruebas de conectividad de red recordando implementar redundancia para evitar dificultades de acceso al sistema.