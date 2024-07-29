from fastapi import FastAPI, Request
from server.controllers import mongo_controller, openai_controller
from server.utils.logger import generate_request_id, RequestIdFilter, logger
import uvicorn

app = FastAPI()

app.include_router(openai_controller.router)
app.include_router(mongo_controller.router)


@app.middleware("http")
async def log_req_res(request: Request, call_next):
    request_id = generate_request_id()
    logger.addFilter(RequestIdFilter(request_id))

    # Log the request details
    body = await request.body()
    logger.info(
        f"Request: {request.method} {request.url} - Headers: {dict(request.headers)} - Body: {body.decode('utf-8')}")

    # Process the request and get the response
    response = await call_next(request)

    # Log the response details
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    logger.info(f"Response: {response.status_code} - Body: {response_body.decode('utf-8')}")

    logger.removeFilter(RequestIdFilter(request_id))
    return response


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello, World!"}


if __name__ == "__main__":

    logger.info("Starting FastAPI server")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
    finally:
        logger.info("FastAPI server shutdown")
