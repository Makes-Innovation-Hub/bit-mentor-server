from fastapi import FastAPI, Request
from server.controllers import mongo_controller, openai_controller, question_controller

app = FastAPI()

app.include_router(openai_controller.router)
app.include_router(mongo_controller.router)
app.include_router(question_controller.router, prefix="/questions", tags=["questions"])


@app.middleware("http")
async def log_req(request: Request, call_next):
    print(f'got req. to: {request.url}, method: {request.method}')
    response = await call_next(request)
    return response


@app.get("/")
def root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
