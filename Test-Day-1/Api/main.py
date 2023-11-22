from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from Config.Connection import mongo_connected

def intialize_app():
    
    @asynccontextmanager
    async def lifespan(app:FastAPI):
        print("Application is Starting")
        mongo_connected.database("TGR")
        
        yield
        
        print("Application is shutting down")
    
    app = FastAPI(lifespan=lifespan)
    
    @app.get("/")
    def home():
        return {"message":"welcome"}

    from Controller.water import router as water_router
    app.include_router(water_router)
    
    return app

app = intialize_app()

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=80)