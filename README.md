# instinct-smoke

Minimal smoke-test app, Python stdlib only, zero dependencies.

## Run

    python3 app.py

Listens on `PORT` (default 3000), bound to `0.0.0.0`.

- `GET /` -> HTML page showing the hostname (proves where it runs)
- `GET /health` -> `{"ok":true}`
- anything else -> 404

## Docker

    docker build -t instinct-smoke .
    docker run -p 3000:3000 instinct-smoke
