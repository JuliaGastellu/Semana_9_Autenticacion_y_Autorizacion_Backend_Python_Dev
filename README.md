# Pulse API — Entrega de la semana 9

En esta entrega amplié la API de la semana 8 con autenticación y autorización completas. Mantengo PostgreSQL, SQLAlchemy asíncrono, Alembic, la separación por capas y todas las validaciones que fui incorporando desde las semanas anteriores.

## Lo que implementé

- Registro y login con hash seguro de contraseñas mediante `pwdlib`.
- Access tokens JWT de corta duración y refresh tokens rotativos persistidos como hash.
- Detección de reutilización, revocación al cerrar sesión y vencimiento configurable.
- Roles `admin`, `editor` y `user`, aplicados con dependencias reutilizables.
- Lectura pública de posts publicados y usuario opcional para acceder a borradores autorizados.
- Reglas de propiedad: un editor modifica sus posts y cada usuario sus comentarios; el admin puede administrar todo.
- Cuatro migraciones acumulativas: baseline, `comments.updated_at`, `hashed_password` y `refresh_tokens`.

## Cómo lo ejecuto

```bash
uv sync
copy .env.example .env
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

Antes de iniciar cambio `JWT_SECRET` por un valor largo y privado. La documentación queda en `http://127.0.0.1:8000/docs`; desde el botón **Authorize** puedo obtener y usar el access token.

## Flujo que pruebo

1. Me registro con `POST /auth/register`.
2. Inicio sesión con `POST /auth/token` usando formulario OAuth2.
3. Consulto `GET /auth/me` con el access token.
4. Renuevo la sesión con `POST /auth/refresh`; el token anterior queda revocado.
5. Cierro la sesión con `POST /auth/logout`.

No guardo contraseñas ni refresh tokens en texto plano. También devuelvo `401` cuando la identidad no es válida y `403` cuando la identidad existe pero no tiene permisos.
