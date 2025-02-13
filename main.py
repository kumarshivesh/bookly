# main.py
from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router 
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import register_all_errors
from src.middleware import register_middleware

# st run http://localhost:8000/api/v1/openapi.json --checks all --experimental=openapi-3.1

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting...")
    await init_db()
    yield
    print("Server has ben stopped...")

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description=" A REST API for a  book review services",
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Kumar Shivesh",
        "url": "https://github.com/kumarshivesh",
        "email": "kumarshiveshch020@gmail.com",
    },
    terms_of_service="https://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs", # http://127.0.0.1:8000/api/v1/docs
    redoc_url=f"{version_prefix}/redoc", # http://127.0.0.1:8000/api/v1/redoc
)

register_all_errors(app)

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])

