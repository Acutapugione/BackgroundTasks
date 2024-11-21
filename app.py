from typing import Annotated
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from time import sleep
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    # Replace with your client's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_progress_updates(filename: str = ""):
    for i in range(10):
        yield f"Processing {filename}: {i * 10}% complete\n"
        sleep(1)
    yield f"Processing {filename}: 100% complete\n"


async def process_file_with_progress(
    filename: str,
    background_tasks: BackgroundTasks,
):

    background_tasks.add_task(generate_progress_updates, filename=filename)

    try:
        # Simulate file processing logic
        sleep(1)
        return f"File {filename} processed successfully!"
    except Exception as e:
        return f"Error processing file {filename}: {str(e)}"


@app.post("/uploadfile_with_progress/")
async def create_upload_file_with_progress(
    background_tasks: BackgroundTasks,
    file: UploadFile,
):
    background_tasks.add_task(
        process_file_with_progress,
        filename=file.filename,
        background_tasks=background_tasks,
    )
    # return StreamingResponse(generate_progress_updates(), media_type="text/plain")
    return StreamingResponse(
        generate_progress_updates(), media_type="text/event-stream"
    )
