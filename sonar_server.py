import asyncio
import websockets
import json

async def receive_sonar_data(websocket):
    print("\n📱 iPhone successfully connected to Sonar System!")
    baseline = None
    
    async for message in websocket:
        try:
            data = json.loads(message)
            volume = data.get("volume", 0)
            
            if baseline is None:
                baseline = volume
                print(f"✅ Calibrated! Quiet baseline room volume: {baseline:.4f}")
                continue
                
            change = abs(volume - baseline)
            
            if change > 0.015:
                print(f"🚨 MOTION DETECTED! Echo Shift: {change:.4f} (Vol: {volume:.4f})")
            else:
                print(f"🟢 Still... (Vol: {volume:.4f})", end="\r")
                
        except Exception as e:
            print(f"Error reading data: {e}")

async def main():
    server = await websockets.serve(receive_sonar_data, "0.0.0.0", 8765)
    print("💻 Windows Sonar Server running. Waiting for iPhone connection...")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
