from fastapi import FastAPI, Request, HTTPException #Request: needed to access request data in handlers
from fastapi.openapi.utils import get_openapi #used to customize the OpenAPI schema (for Swagger docs)
from dotenv import load_dotenv #Imports function to load environment variables from a .env file
#importing routes 
from app.auth.routes import router as auth_router
from app.products.routes import admin_router, public_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router

from app.core.error_handler import http_exception_handler, unhandled_exception_handler
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

load_dotenv() #Loads all variables from .env into the environment.

app = FastAPI() #Creates an instance of the FastAPI application.
#including routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(public_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(orders_router)

#Customizes Swagger UI to include JWT Bearer token authentication in docs.
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-commerce Backend System API",
        version="1.0.0",
        description="API with JWT Bearer Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_exception_handler(HTTPException, http_exception_handler) #Tells FastAPI to use http_exception_handler for any HTTPException
app.add_exception_handler(Exception, unhandled_exception_handler)#Catches all other uncaught exceptions and sends a consistent error response.
