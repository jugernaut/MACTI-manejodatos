# 🚀 Guía de Despliegue en Render.com

## Archivos del proyecto

```
portafolio-app/
├── app.py               ← App principal de Streamlit
├── requirements.txt     ← Dependencias de Python
└── README.md            ← Este archivo
```

---

## Paso 1: Subir a GitHub

1. Crea un repositorio nuevo en [github.com](https://github.com) (puede ser público o privado)
2. Sube los archivos:

```bash
git init
git add app.py requirements.txt
git commit -m "Portafolio conservador - primera versión"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

---

## Paso 2: Crear el servicio en Render

1. Ve a [render.com](https://render.com) y crea una cuenta gratuita
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu cuenta de GitHub y selecciona el repositorio
4. Configura el servicio:

| Campo | Valor |
|-------|-------|
| **Name** | `portafolio-conservador` (o el que quieras) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

5. En **Instance Type** selecciona **Free** (suficiente para la clase)
6. Haz clic en **"Create Web Service"**

⏳ El deploy tarda ~3–5 minutos la primera vez.

---

## Paso 3: Acceder a la app

Una vez desplegada, Render te dará una URL pública como:

```
https://portafolio-conservador.onrender.com
```

¡Comparte esa URL con tus compañeros y profesor! 🎉

---

## ⚠️ Notas importantes

- **Plan gratuito de Render:** El servicio se "duerme" después de 15 minutos de inactividad.
  La primera visita tras ese período tarda ~30 segundos en cargar (es normal).
- **Datos en caché:** La app cachea los datos de Yahoo Finance por 1 hora para no sobrecargar la API.
- **Para actualizar la app:** Solo haz `git push` al repositorio y Render redespliega automáticamente.

---

## Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Verifica que el módulo esté en `requirements.txt` |
| App no carga datos | Yahoo Finance puede tener delays; recarga la página |
| Error de puerto | Asegúrate que el Start Command incluya `--server.port $PORT` |
| Build falla | Revisa los logs en el dashboard de Render |

---

## Comandos para probar localmente antes de subir

```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr la app localmente
streamlit run app.py

# Se abrirá en: http://localhost:8501
```
