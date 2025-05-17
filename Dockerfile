# Usa una imagen oficial con uv y Python 3.12
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Establece el directorio de trabajo
WORKDIR /app

# Opciones recomendadas para compilación y copia
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Instala las dependencias desde los archivos bloqueados
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copia el resto del código del proyecto
COPY . /app

# Instala el proyecto sin dependencias de desarrollo
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Asegura que los ejecutables de uv estén en el PATH
ENV PATH="/app/.venv/bin:$PATH"

# Elimina el entrypoint por defecto
ENTRYPOINT []

# Expone el puerto por defecto de Streamlit
EXPOSE 8501

# Ejecuta Streamlit como comando principal usando uv
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
