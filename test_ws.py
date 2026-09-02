import asyncio
import websockets

async def test():
    uri = "ws://localhost:8000/ws/progress/test_session"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected")
            # Wait for a message (but none will be sent unless pipeline runs)
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print("Received:", msg)
            except asyncio.TimeoutError:
                print("No message received within 5 seconds")
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
