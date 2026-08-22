import asyncio
import wavelink
import os

async def main():
    print("Connecting to node...")
    node = wavelink.Node(uri='http://lava2.kasawa.pro:2334', password='youshallnotpass')
    await wavelink.Pool.connect(nodes=[node], client=None, cache_capacity=100)
    print("Connected.")
    
    query = "Bandeya"
    print(f"Searching for: {query}")
    
    print("1. Default search")
    try:
        tracks = await wavelink.Playable.search(query)
        print(f"Found: {len(tracks)}")
        if tracks: print(f"First: {tracks[0].title}")
    except Exception as e:
        print(f"Error: {e}")

    print("2. scsearch:")
    try:
        tracks = await wavelink.Playable.search(f"scsearch:{query}")
        print(f"Found: {len(tracks)}")
        if tracks: print(f"First: {tracks[0].title}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
