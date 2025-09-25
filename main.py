import asyncio
from art import tprint
from fastapi import FastAPI
from routers import api_router
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from apps.modules.emails.rabbitmq import RabbitMQHandler


tprint("APP-API-MAKEUP", font="slant")

app = FastAPI(
    title="APP-API-MAKEUP",
    version="1.0.0",
    description="RestfulAPI backend with JWT authentication",
)

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Dev quèn",
        "url": "https://dcbao.com/",
        "email": "dcbao.dev@gmail.com"
    }
    openapi_schema["info"]["termsOfService"] = "https://www.linkedin.com/in/dcbao/"

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **'Bearer <JWT>'**, where JWT is the access token"
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]: 
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(api_router)
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
@app.on_event("startup")
async def startup_event():
    rabbit = RabbitMQHandler()
    asyncio.create_task(rabbit.consumer())
    print("[*] RabbitMQ consumer started ✅")