# Guía de Instalación y Configuración - Sistema de Tutoría CLI

Esta guía detalla los pasos necesarios para instalar, configurar y poner en marcha el Sistema de Tutoría Personalizado por CLI conectado a Google Gemini.

---

## 1. Requisitos Previos
- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API de **Google Gemini** (`GEMINI_API_KEY`). Puedes obtenerla en [Google AI Studio](https://aistudio.google.com/).

---

## 2. Instalación de Dependencias
Abre una terminal en la carpeta raíz del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias (`google-generativeai`, `python-dotenv`, `pypdf`, etc.):

```bash
pip install -r requirements.txt
```

---

## 3. Configuración de Variables de Entorno
1. Duplica el archivo `.env.example` y renómbralo a `.env`, o crea un archivo nuevo llamado `.env` en la raíz del proyecto.
2. Agrega tu clave de API de Gemini con el siguiente formato:

```env
GEMINI_API_KEY=tu_api_key_de_google_gemini_aqui
```

---

## 4. Ejecución del Sistema
Puedes iniciar el tutor ejecutando el archivo batch (en Windows):
```cmd
iniciar_tutor.bat
```
O directamente desde la terminal con Python:
```bash
python main.py
```
