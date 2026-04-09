from fastapi import FastAPI
from app.api import upload, recognition, search, export

app = FastAPI(title="Enterprise Registry Search System")

app.include_router(upload.router, prefix="/api/upload")
app.include_router(recognition.router, prefix="/api/recognition")
app.include_router(search.router, prefix="/api/search")
app.include_router(export.router, prefix="/api/export")

@app.get("/health")
def health_check():
    return {"status": "ok"}
