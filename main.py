from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return JSONResponse(content={
        "message": "API is running", 
    }, status_code=200)

# Health endpoint
@app.get("/health")
async def health():
    return JSONResponse(content={
        "message": "healthy"
    }, status_code=200)
    
#
@app.get("/me")
async def me():
    return JSONResponse(content={
        "name": "Divine Obido",
        "email": "divineobido64@gmail.com",
        "github": "https://github.com/DivineObido"
    }, status_code=200)