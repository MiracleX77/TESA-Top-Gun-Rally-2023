from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#import logging
from contextlib import asynccontextmanager
from Config.Connection import mongo_connected

def intialize_app():
    
    @asynccontextmanager
    async def lifespan(app:FastAPI):
        print("Application is Starting")
        mongo_connected.database("TGR")
        
        yield
        
        print("Application is shutting down")

    #logging.basicConfig(level=logging.INFO, filename='/app/logs/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

    
    app = FastAPI(lifespan=lifespan)
    
    origins = [
    "http://192.168.1.61",  
    "http://192.168.1.62",
    "http://192.168.1.63"      
    ]

    app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    @app.get("/")
    def home():
        return {"message":"welcome"}

    from Controller.water import router as water_router
    app.include_router(water_router)
    from Controller.predict_water import router as predict_water_router
    app.include_router(predict_water_router)
    from Controller.sensor import router as sensor_router
    app.include_router(sensor_router)
    
    return app

app = intialize_app()

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=80)
    #uvicorn.run(app,host="127.0.0.1",port=80)