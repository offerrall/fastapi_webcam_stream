from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from contextlib import asynccontextmanager
import cv2
import sys

def create_app(device_path: str) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        camera = cv2.VideoCapture(device_path)
        app.state.camera = camera
        app.state.running = True
        yield
        app.state.running = False
        if camera.isOpened():
            camera.release()
            print(f"Camera {device_path} released.")

    app = FastAPI(lifespan=lifespan)

    def generate_frames():
        camera = app.state.camera
        while app.state.running:
            success, frame = camera.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    @app.get("/", response_class=HTMLResponse)
    def index():
        return """
        <html>
            <head><title>Webcam Stream</title></head>
            <body>
                <h1>Webcam Stream</h1>
                <img src="/video">
            </body>
        </html>
        """

    @app.get("/video")
    def video():
        return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

    return app

if __name__ == "__main__":
    import uvicorn
    if len(sys.argv) < 3:
        print("Uso: python3 main.py /dev/videoX PUERTO")
        sys.exit(1)
    device = sys.argv[1]
    port = int(sys.argv[2])
    uvicorn.run(lambda: create_app(device), host="0.0.0.0", port=port)
