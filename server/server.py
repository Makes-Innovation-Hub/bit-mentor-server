from fastapi  import FastAPI, Request
from controllers import topic_controller

app = FastAPI()

app.include_router(topic_controller.router)

@app.middleware("http")
async def log_req(request:Request, call_next):
    print(f'got req. to: {request.url}, method: {request.method}')
    response = await call_next(request)
    return response

@app.get("/")
def root():
    return {"message": "Hello from FastApi"}

