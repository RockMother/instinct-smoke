# instinct-smoke

A deliberately tiny **web application** used as a smoke test: can an AI agent
clone a public repository and get it running on a host it controls?

It has no dependencies, no database, no build step and no secrets. It is a
single Python file that starts an HTTP server. If it answers, the whole
chain worked: repository access → code understood → process started → port
reachable from outside.

## What the application does

An HTTP server with three behaviours:

- `GET /` → HTML page containing the word `instinct-smoke` and the **hostname**
  of the machine it runs on
- `GET /health` → `{"ok":true}` (plain JSON)
- anything else → HTTP `404`

The hostname on `/` is the point of the test: it proves *where* the app is
actually running, which a "looks fine" screenshot cannot.

## Requirements

- Python 3.8 or newer. Nothing else — no `pip install`, no `npm install`.
- One open TCP port, taken from the `PORT` environment variable (default `3000`).
- The process must bind `0.0.0.0`, not `127.0.0.1`, or it will not be reachable
  from outside the machine.

## Run it

```bash
git clone <this-repo-url>
cd instinct-smoke
PORT=3000 python3 app.py
```

The server prints `listening on :3000` and then serves. It runs in the
foreground by design.

If the process must survive after your session ends, run it under a supervisor
(`systemd`, `tmux`, `nohup`, or the platform's own process manager) — a bare
`python3 app.py &` in a shell that exits usually gets reaped with the shell.

## Verify it

From inside the host:

```bash
curl -s localhost:3000/health      # -> {"ok":true}
```

From outside the host — this is the real test:

```bash
curl -s <public-url>/health        # -> {"ok":true}
curl -s <public-url>/              # -> HTML with the hostname
```

Both must succeed. `localhost` working while the public URL fails means the
port is not exposed, not that the app is broken.

## Run with Docker (optional)

```bash
docker build -t instinct-smoke .
docker run -p 3000:3000 instinct-smoke
```

The image is `python:3.12-alpine` with a single `COPY`. Use it only if Docker
is already available on the host — plain `python3` works everywhere and starts
faster.

## Notes

- No external network calls at runtime. If it fails, the problem is the process
  or the network path, never a third-party service.
- No state. Safe to kill and restart at any time.
- Nothing secret in this repository. It is intentionally public.
