import asyncio
import websockets
from PIL import Image, UnidentifiedImageError

def is_valid_image(image_bytes):
    try:
        Image.open(image_bytes)
        return True
    except (UnidentifiedImageError, OSError):
        return False

async def handle_connection(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            if is_valid_image(message):
                with open("image.jpg", "wb") as f:
                    f.write(message)
                    print("Image saved")
            else:
                print("Invalid image received")
        except websockets.exceptions.ConnectionClosed:
            break

async def main():
    server = await websockets.serve(handle_connection, '0.0.0.0', 3001)  # Replace 3001 with your desired port number
    await server.wait_closed()

asyncio.run(main())