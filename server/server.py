from fastapi import FastAPI, Request, Response

from model.YouTube_DB import get_db
from server.utils.logger import app_logger, RequestIdFilter, generate_request_id
from server.controllers import mongo_controller, openai_controller, question_controller,youtube_controller

app = FastAPI()
app.include_router(mongo_controller.router)
app.include_router(question_controller.router, prefix="/questions", tags=["questions"])
app.include_router(youtube_controller.router, prefix="/youtube", tags=["youtube"])
app.include_router(openai_controller.router)


@app.middleware("http")
async def log_req(request: Request, call_next):
    request_id = generate_request_id()
    request.state.request_id = request_id
    request_id_filter = RequestIdFilter(request_id)
    app_logger.addFilter(request_id_filter)
    app_logger.info(f"Received request: URL={request.url}, Method={request.method}")
    try:
        response = await call_next(request)
    except Exception as e:
        app_logger.error(f"Exception during request handling: {e}", exc_info=True)
        response = Response(content="Internal server error", status_code=500)
    finally:
        app_logger.info(f"Response status: {response.status_code} for URL={request.url}")
        app_logger.removeFilter(request_id_filter)
    return response


@app.get("/")
def root():
    app_logger.info("Root endpoint called")
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
