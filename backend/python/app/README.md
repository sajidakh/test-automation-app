# app (models / services / routers)
- **models**: Pydantic contracts (validate input/output)
- **services**: business logic (pure, unit-test friendly)
- **routers**: FastAPI routes that validate at the edge and call services