# FastAPI Webcam Streamer

Stream multiple webcams over your local network using FastAPI and OpenCV (Linux and Windows)

## 🔧 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- OpenCV

### Install dependencies

```bash
pip install fastapi uvicorn opencv-python
```

## 🚀 Usage

```bash
python3 main.py /dev/video0 8501
```

Supports absolute paths like:

```bash
python3 main.py /dev/v4l/by-id/usb-Logitech_HD_Pro_Webcam_C920-video-index0 8501
```

A numeric index (e.g. 0, 1, etc.). In this case, OpenCV will automatically select the webcam at that index:
```bash
python3 main.py 0 8501
```

## 🌐 View the stream

Open in your browser:

```
http://YOUR_SERVER_IP:8501
```

## 💡 Notes

- Each camera needs a separate port.
- `/dev/v4l/by-id/...` paths are recommended for multiple identical webcams.
- Cameras are released cleanly on shutdown.

## 📦 Download

```bash
git clone https://github.com/your-username/webcam-streamer.git
cd webcam-streamer
```

## 📝 License

MIT
