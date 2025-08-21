# backend/python
FastAPI backend with typed settings, strict CORS, deterministic tests, and clear observability.

- `main.py`: app factory, middlewares, error envelope
- `settings.py`: typed config; CORS parsing (CSV or JSON) with safe defaults
- `observability.py`: JSON logs, request-id propagation, error shaping
- `security.py`: simple API-key guard + security headers
- `app/`:
  - `models/`: Pydantic request/response contracts
  - `services/`: pure business logic (easy to unit-test)
  - `routers/`: thin controllers mapping HTTP → services
- `tests/`: unit + live stages (see markers below)