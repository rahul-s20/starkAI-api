from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=5001)