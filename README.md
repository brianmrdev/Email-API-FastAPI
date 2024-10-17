
# Email API - FastAPI

Esta es una API para el envío de correos electrónicos utilizando **FastAPI** y **SMTP**. La API está protegida mediante un token de autorización y limita la cantidad de solicitudes por minuto por dirección IP. Además, el contenido HTML de los correos se sanitiza para evitar inyecciones maliciosas.

## Features

- **Envío de correos electrónicos**: La API permite enviar correos electrónicos mediante una conexión segura SMTP.
- **Protección mediante token**: Acceso protegido con Bearer Token para seguridad en el envío de correos.
- **Sanitización de HTML**: Sanitización del contenido HTML con `bleach` para evitar vulnerabilidades XSS.
- **Rate Limiting**: Límite de 2 solicitudes por minuto por IP, configurable.
- **Logging**: Registro de los eventos importantes y errores en un archivo de log.
- **Validación de entradas**: Validación de los correos electrónicos y estructura del mensaje con Pydantic.

## Instalación

Sigue los pasos a continuación para instalar y ejecutar la API localmente.

### Prerrequisitos

- **Python 3.8+**: Asegúrate de tener Python instalado.
- **Virtualenv**: Es recomendable crear un entorno virtual.

### Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/Email-API-FastAPI.git
cd Email-API-FastAPI
```

### Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

### Instalar dependencias

Instala las dependencias definidas en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Configuración

Debes configurar las siguientes variables de entorno en un archivo `.env` en la raíz del proyecto.

Ejemplo de `.env`:

```env
SMTP_HOST=smtp.tu_dominio.com
SMTP_PORT=587
SMTP_USERNAME=tu_usuario
SMTP_PASSWORD=tu_contraseña
AUTHORIZATION_TOKEN=tu_token_de_autorizacion
```

### Variables de entorno requeridas:

- **SMTP_HOST**: El servidor SMTP que se utilizará para enviar correos.
- **SMTP_PORT**: El puerto del servidor SMTP (587 para TLS).
- **SMTP_USERNAME**: El nombre de usuario para autenticarse en el servidor SMTP.
- **SMTP_PASSWORD**: La contraseña del usuario SMTP.
- **AUTHORIZATION_TOKEN**: Token de autorización Bearer para proteger la API.

## Uso

Para ejecutar la API localmente, usa el siguiente comando:

```bash
uvicorn main:app --reload
```

Esto iniciará la aplicación en `http://localhost:8000`.

### Endpoints

#### POST /send/

Este endpoint permite enviar un correo electrónico. Requiere autenticación mediante un Bearer Token.

- **URL**: `/send/`
- **Método**: `POST`
- **Headers**:
  - `Authorization: Bearer <token>`
- **Body** (JSON):
  
  ```json
  {
    "from_email": "turemitente@ejemplo.com",
    "to_email": ["destinatario1@ejemplo.com", "destinatario2@ejemplo.com"],
    "subject": "Asunto del correo",
    "html": "<p>Contenido HTML del correo</p>"
  }
  ```

#### Ejemplo de curl:

```bash
curl -X POST "http://localhost:8000/send/" \
-H "Authorization: Bearer <tu_token>" \
-H "Content-Type: application/json" \
-d '{
  "from_email": "remitente@ejemplo.com",
  "to_email": ["destinatario@ejemplo.com"],
  "subject": "Prueba de correo",
  "html": "<p>Este es un correo de prueba</p>"
}'
```

## Responses

El API puede devolver las siguientes respuestas HTTP:

- **200 OK**: El correo fue enviado con éxito.
  ```json
  {
    "detail": {
      "message": "Email sent successfully",
      "status": 200
    }
  }
  ```

- **401 Unauthorized**: Token de autorización inválido o no proporcionado.
  ```json
  {
    "detail": {
      "message": "Invalid or missing token",
      "status": 401
    }
  }
  ```

- **429 Too Many Requests**: Se excedió el límite de solicitudes permitidas por IP.
  ```json
  {
    "detail": {
      "message": "Too many requests, please try again later.",
      "status": 429
    }
  }
  ```

- **500 Internal Server Error**: Error al intentar enviar el correo.
  ```json
  {
    "detail": {
      "message": "Error sending email: <detalle_del_error>",
      "status": 500
    }
  }
  ```

### Logs

El archivo de log (`app.log`) almacenará información relevante de los correos enviados y errores en caso de que los haya.

## Rate Limiting

El rate limit está configurado para permitir un máximo de **2 solicitudes por minuto** por IP. Este límite puede ser ajustado modificando el decorador `@limiter.limit` en el archivo `main.py`.

## Testing

Puedes usar `curl`, Postman o cualquier herramienta similar para hacer pruebas de la API.

## Seguridad

- El contenido HTML de los correos es sanitizado para evitar inyecciones maliciosas.
- Las credenciales del servidor SMTP y el token de autorización no deben compartirse ni exponerse públicamente.
- Asegúrate de utilizar conexiones TLS para el envío seguro de correos electrónicos.

## Contribuir

Las contribuciones son bienvenidas. Si deseas agregar nuevas características o corregir errores, por favor, abre un **pull request** o inicia una discusión.

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m "Descripción de los cambios"`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un **pull request**.

## MIT License

Este proyecto está licenciado bajo los términos de la [MIT License](./LICENSE).