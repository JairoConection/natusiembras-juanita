# Natusiembras Juanita - Aplicativo móvil/web

## 1. Crear la base de datos
Abre MySQL y ejecuta `schema.sql`.

## 2. Crear entorno virtual
Windows:
python -m venv venv
venv\Scripts\activate

## 3. Instalar dependencias
pip install -r requirements.txt

## 4. Configurar MySQL
Por defecto usa:
- host: localhost
- usuario: root
- contraseña: vacía
- base: natusiembras

Si tu MySQL tiene otra contraseña, puedes editar `app.py` o usar variables:
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=tu_clave
set DB_NAME=natusiembras

## 5. Ejecutar
python app.py

Luego abre:
http://127.0.0.1:5000

## 6. Próximas mejoras
- Panel administrador.
- Subir fotografías reales de cada hortaliza.
- Categorías.
- Inventario.
- Clientes.
- Pedidos por WhatsApp.
- Historial de pedidos.
- Información nutricional detallada.
- Login de administrador.
- Convertir la PWA en APK Android.
