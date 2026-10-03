---
materia: Internet de las Cosas
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [internet_de_las_cosas, diapositiva, ingesta_ia]
---

[[Internet de las Cosas]]

# Node-red Básico

---

## Recordatorio

1. ¿Qué formato tiene un programa en [[Node-RED]]?
2. ¿Cómo se guarda un flujo?
3. ¿Cómo se puede cargar un flujo del PC?
4. ¿Dónde encontrar nuevos nodos?
5. ¿Cómo instalar nuevos nodos?
6. ¿Para qué sirven los nodos `Inject`, `Debug` y `Function`?
7. Usar la consola `cmd`
8. `>node-red -p 1880 -u C:\nombre de la carpeta`

---

## Problema y Objetivo

* **Problema:** Caracterizar a [[Node-RED]].
* **Objetivo:** Identificar nuevas funcionalidades de [[Node-RED]] a través de la paleta de nodos.

---

## ¿Qué es Node-RED?

* [[Node.js]]
* Event-driven (Orientado a eventos)
* Non-blocking (No bloqueante)
* Asincrónico
* Single thread (Monohilo)
* IO intensive, data-intensive
* Escalable, rápido
* [[JSON]]
* Web editor (Browser)
* Programas $\rightarrow$ flujos de nodos
* Servidor web $\rightarrow$ aplicaciones web

`Node-red -> Node.js -> JavaScript`

### ¿Por qué Node-RED?
* Creado con [[IoT]] en mente
* Corre en todas las capas [[IoT]]
* Curva de aprendizaje corta
* Hobbies $\rightarrow$ Profesional
* Clases virtuales

---

## Flujo de datos

* `Stages = Nodes`
* Helado $\rightarrow$ se modifica en cada `stage`
* `Data` $\rightarrow$ `entra` $\rightarrow$ `modifica` $\rightarrow$ `sale` de cada nodo en el flujo

### Data:
* `Msg` $\rightarrow$ Lote
* `Id` $\rightarrow$ Identificación única
* `Topic` $\rightarrow$ Descripción producto
* `Payload` $\rightarrow$ Producto

> **Diagrama detectado:** Ilustración conceptual que compara una línea de producción industrial (etapas de *Blending* y *Pasteurization* con cajas y un carrito de compras con helados) con la estructura de un objeto JavaScript `msg` que contiene las propiedades `Id`, `Topic` y `Payload`.

---

## Ejercicio 1

En un nuevo Tab, haga un nuevo flujo que cubra los siguientes requerimientos:

1. Simule un sensor generando datos aleatorios con valores reales, para esto hay que instalar un nuevo nodo `Random`. Utilice un `inject` para generar un dato aleatorio cada vez que de click y muestre el dato en el `debug`.
2. Convierta la salida en unidades de ingeniería. Por ejemplo, multiplicar el dato aleatorio por 10 y eso sería la simulación de temperatura.
3. El mismo dato aleatorio lo podemos multiplicar por 3 y sumarle 2.5, y esto podría ser el valor simulado de humedad.
4. Cada sensor simulado debe salir por un `debug` diferente (salidas diferentes).
5. Vamos a comparar el valor de temperatura y si es mayor que 50, generamos un texto de Alarma. (Alarma mayor a 50).
6. Repetimos lo mismo y si la humedad es mayor 90, el texto sería: Alarma mayor a 90.

---

## Metodología

* Instalar nodo $\rightarrow$ `random` y verificar que funciona.
* Operaciones matemáticas, que no sean de decisiones lógicas se recomienda usar en nodo $\rightarrow$ `function`.
* Recordar usar `debug` $\rightarrow$ `complete`, para ver todo el objeto.
* Dentro del nodo `function`, se puede usar todas las funcionalidades de [[JavaScript]].

```javascript
var randomValue = msg.payload;
msg.payload = (randomValue * 10); 
return msg;
```

```javascript
var randomValue = msg.payload;
msg.payload = ((randomValue * 3) + 2.5); 
return mail; // (Nota: en la diapositiva original aparece como return msg;)
```

```javascript
if (msg.payload > 50) { 
    msg.payload = "Alarma mayor a 50";
} else { 
    msg = null;
}
return msg;
```

---

## Ejercicio 2

* Ajustar decimales $\rightarrow$ `.toFixed(2)`
* Resolver la lógica de las alarmas sin usar el nodo `function`.
* Sugerencia: Usar los nodos: `switch` y `change`.

---

## Ejercicio 3

* Crear un [[JSON]] con el `inject` y verlo en el `debug`:
  `{ "temp": 23, "hum": 88, "name": "pepito"}`
* Extraer las variables `temp`, `hum` y `name` del objeto y mostrarlos en `debug` diferentes.
* Sugerencia, usar el nodo: `change`.
* A la salida del nodo de temperatura, añadir una nueva propiedad, por ejemplo `ciudad` y además, modificar el `topic`.

> **Diagrama detectado:** Captura de pantalla del editor de flujos de Node-RED mostrando un nodo `inject` conectado a tres ramas paralelas: un nodo `debug` directo, un nodo `change` (*set msg.payload*) que alimenta un nodo de temperatura con su respectivo `debug`, y una derivación inferior con un nodo `change` de 2 reglas que conecta con un nodo `debug` etiquetado como *new2*.