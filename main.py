from app import create_app
import uvicorn

original_callback = uvicorn.main.callback


def callback(**kwargs):
    from celery.contrib.testing.worker import start_worker
    from app.pipelines.migration.csv_to_db import tasks

    with start_worker(tasks.celery_app, perform_ping_check=False, loglevel="info"):
        original_callback(**kwargs)


uvicorn.main.callback = callback

app = create_app()

if __name__ == "__main__":
    uvicorn.main()
