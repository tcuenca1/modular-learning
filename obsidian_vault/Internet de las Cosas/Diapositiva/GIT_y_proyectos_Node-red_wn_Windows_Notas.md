---
materia: [[Internet de las Cosas]]
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [internet_de_las_cosas, diapositiva, ingesta_ia]
---

# Tutorial para trabajar con proyectos en [[Node-RED]] y [[GitHub]]

## Configuraciones para [[GitHub]]

1. Crear una cuenta de [[GitHub]] con un email válido.
2. Instalar [[Git]] en el PC ([Sitio oficial de Git](https://www.git-scm.com/downloads)).

> **Captura de pantalla:** Menú de inicio de Windows mostrando la aplicación [[Git Bash]] seleccionada para su ejecución.

Abrimos el [[Git]] (`Git Bash`) y realizamos los siguientes comandos:

```bash
cd ~
mkdir -p ~/.ssh
touch ~/.ssh/known_hosts
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
nano ~/.ssh/known_hosts
```

* **Verificar el contenido:** Deberías ver una línea que comienza con `github.com` seguida de una clave SSH.

> **Captura de pantalla:** Consola de [[Git Bash]] ejecutando los comandos SSH para la creación y escaneo de llaves hacia el archivo `known_hosts`.

> **Captura de pantalla:** Explorador de archivos mostrando la ruta `.ssh` con los archivos `known_hosts` y `known_hosts.old`.

> **Captura de pantalla:** Editor `nano` dentro de [[Git Bash]] mostrando la clave SSH almacenada correctamente para `github.com`.

---

## Configuraciones para [[Node-RED]]

1. Habilitar los proyectos en [[Node-RED]]. Para ello debemos ir a la carpeta de [[Node-RED]] en Windows y editar el archivo `settings.js`, cambiando el siguiente parámetro:

```javascript
Projects: {
    Enabled: true,
    // ...
}
```

Como ya sabemos, podemos tener nuestros flujos en la carpeta por defecto de [[Node-RED]] situada en:
* `C:\Users\[ESTUDIANTE]\.node-red`
* O bien en una carpeta predefinida (por ejemplo: `C:\Node-red-1880`).

> **Captura de pantalla:** Entorno de edición del archivo `settings.js` en [[Node-RED]] resaltando la propiedad `enabled: true` dentro del objeto `Projects`.

2. Crear un nuevo repositorio en [[GitHub]] (probablemente requiera [[Autenticación de Dos Factores]]).

> **Captura de pantalla:** Interfaz web de [[GitHub]] mostrando el perfil del usuario y el botón verde "New" para la creación de un repositorio.

Al presionar **New**, creamos un nuevo repositorio (ej. `-- >UPSE`).

> **Captura de pantalla:** Página de configuración del repositorio en [[GitHub]] resaltando el enlace de clonación mediante el protocolo [[SSH]]: `git@github.com:[ESTUDIANTE]/UPSE.git`.

3. Copiamos la URL de [[SSH]] para conectarnos desde [[Node-RED]].

4. Configuramos la conexión con [[Git]] desde [[Node-RED]]. Para eso debemos ir a **Settings** > **Git config** y configurar la siguiente metadata:

> **Captura de pantalla:** Ventana de comandos de Windows ejecutando la instancia de [[Node-RED]] en el puerto 1880 con la carpeta personalizada: `node-red -p 1880 -u C:\Node-red-1880`.

> **Captura de pantalla:** Menú de ajustes en [[Node-RED]] y panel de configuración de [[Git]] (*Committer Details*).

* **Username:** Nombre de tu cuenta de [[GitHub]] (ej. `iotinfodixys`).
* **Email:** Email asociado a la cuenta de [[GitHub]] (`[ESTUDIANTE]@gmail.com`).
* **Workflow:** `manual`.
* **SSH Key:** Aquí vamos a crear una clave, por tanto seleccionamos **add key**.

> **Captura de pantalla:** Formulario "Add SSH Key" solicitando un nombre (*Name*) y una frase de contraseña opcional (*Passphrase*).

* **Name:** Se le asigna un nombre (ej. `test2` o `UPSE`).
* **Passphrase:** Se deja vacío.
* Presionamos el botón **Generate key** para generar el par de claves.

> **Captura de pantalla:** Clave pública RSA generada en [[Node-RED]] con el botón inferior "Copy public key to clipboard".

5. Copiamos dicha clave para agregarla en la cuenta de [[GitHub]] y así lograr un enlace bidireccional entre [[Node-RED]] y [[GitHub]].

> **Captura de pantalla:** Menú desplegable de usuario en [[GitHub]] seleccionando **Settings**.

> **Captura de pantalla:** Menú de configuración de la cuenta en [[GitHub]] resaltando la opción **SSH and GPG keys**.

6. Creamos una nueva clave SSH en [[GitHub]]:
   * Damos clic en **New SSH key**.
   * Rellenamos el campo **Title** y en **Key** pegamos la clave generada desde [[Node-RED]].
   * Añadimos la clave presionando **Add SSH key**.

> **Captura de pantalla:** Interfaz de [[GitHub]] mostrando la lista de llaves SSH asociadas con su respectiva huella digital (*fingerprint*).

7. Desde [[Node-RED]], creamos un nuevo proyecto.

> **Captura de pantalla:** Menú superior de [[Node-RED]] desplegando las opciones de proyectos (*New*, *Open*, *Project Settings*).

> **Captura de pantalla:** Formulario de creación de proyectos en [[Node-RED]] (*Project name*, *Description*, *Flow file*, *Credentials*).

* El campo **Project name** debe mostrarse habilitado (en azul).
* Si buscamos en **Project Settings**, veremos la configuración general de dependencias y control de versiones.

> **Captura de pantalla:** Configuración de repositorios remotos (*Git remotes*) en [[Node-RED]].

* **Remote name:** `origin`
* **URL:** La clave [[SSH]] o URL del repositorio de [[GitHub]].
* Luego hacemos clic en **Add remote**.

---

## Control de Versiones y Sincronización ([[Commit]] y [[Push]])

9. Una vez enlazado el proyecto de [[Node-RED]] con el repositorio de [[GitHub]], creamos un flujo, hacemos un **Deploy**, realizamos un **Commit** y posteriormente un **Push**.

> **Captura de pantalla:** Interfaz de [[Node-RED]] destacando el icono de [[Git]] ubicado en el panel lateral derecho.

> **Captura de pantalla:** Secuencia de ventanas en el panel de [[Git]] de [[Node-RED]]: selección de archivos locales con el botón **+all**, área de preparación para el *Commit* y campo de texto para el comentario.

* **Local files:** Muestra los archivos modificados (ej. `flows.json`). Presionamos **+all**.
* **Commit:** Ingresamos un texto descriptivo para el historial de versiones.

> **Captura de pantalla:** Historial de commits en [[Node-RED]] mostrando los registros locales y el botón de sincronización de rama (*Push*).

* **Push:** Para enviar los cambios a la nube, vamos al historial de commits y seleccionamos **Remote: origin/master**.
* La primera vez aparecerá un cuadro de diálogo pidiendo credenciales o confirmación, en el cual presionamos **Retry**.

> **Captura de pantalla:** Cuadro de diálogo de autenticación requerida para el repositorio remoto en [[Node-RED]] con el botón **Retry**.

11. Verificamos que los cambios se hayan reflejado correctamente ingresando al repositorio en [[GitHub]].

> **Captura de pantalla:** Historial de commits en la interfaz web de [[GitHub]] mostrando el mensaje del commit realizado (*tu comentario*).

---

> **Nota importante:** Antes de empezar a trabajar en un equipo o sesión diferente, asegúrate de realizar un **PULL** para sincronizar los últimos cambios del repositorio remoto hacia tu instancia local de [[Node-RED]].