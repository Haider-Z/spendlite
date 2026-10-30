from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app.routes.expenses import router as expenses_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpendLite API")

# Serve CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Load HTML templates
templates = Jinja2Templates(directory="app/templates")

# Register API routes
app.include_router(expenses_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
def health_check():
    return {"status": "healthy"}
