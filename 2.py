from mutagen.oggopus import OggOpus
import base64
import os

# Load image for embedding
with open("my_art.png", "rb") as img_file:
    art_base64 = base64.b64encode(img_file.read()).decode('utf-8')

# Opus cover art (base64-encoded FLAC-style picture block)
picture_block = f'''
metadata_block_picture={base64.b64encode(
    b'\x03' +  # picture type: front cover (3)
    b'\x00\x00\x00\x00' +  # MIME type (empty for auto)
    b'\x00\x00\x00\x00' +  # description (empty)
    b'\x00\x00\x00\x80' +  # width
    b'\x00\x00\x00\x80' +  # height
    b'\x00\x00\x00\x08' +  # depth
    b'\x00\x00\x00\x00' +  # colors
    len(base64.b64decode(art_base64)).to_bytes(4, 'big') +  # image data length
    base64.b64decode(art_base64)  # actual image
).decode("utf-8")}
'''.strip()

# List of untagged files
missing_files = [
    "AWAITED.opus", "Adult Empire Strikes Back.opus", "As Long As You Are Here With Me.opus",
    "Because You Are Here.opus", "Classic Theme 1.opus", "Classic Theme 2.opus",
    "DEPTH OF SORROW.opus", "Depth Of Sorrow 2.opus", "Depth Of Sorrow 3.opus",
    "Furious Attack.opus", "Goodbye Kiiboo.opus", "Goodbye Peko.opus", "Goodbye Pippo.opus",
    "Hiroshi's Reminiscence.opus", "Island Of Miracles.opus", "Legend Of Mermaid.opus",
    "Legendary Underwater City.opus", "Let Me Hear Your Dreams.opus", "Marriage.opus",
    "Meeting Peko.opus", "Miracle Light.opus", "Nobita And Pippo.opus", "Peko's Promise.opus",
    "Phantom DOREX Is Here.opus", "Phantom DoraX Vs Guard Robo.opus", "Promise.opus",
    "Resurrection Of The Gigantic Statue.opus", "Riruru And Shizuka.opus", "Riruru's Memory.opus",
    "Sparrow Jack.opus", "Thankyou Shizuka.opus", "The End Of Zanda Claus.opus", "Theme 1.opus",
    "Theme 2.opus", "Treasure Island 1.opus", "Treasure Island 2.opus", "Watting.opus",
    "Your Laughing World.opus", "Zanda Claus Suite.opus"
]

for filename in missing_files:
    try:
        audio = OggOpus(filename)
        audio["title"] = filename.replace(".opus", "")
        audio["artist"] = "Varun"
        audio["album"] = "Varun Vibes"
        audio["comment"] = "Tagged by Varun 🛠️"
        audio["metadata_block_picture"] = picture_block
        audio.save()
        print(f"✅ Tagged: {filename}")
    except Exception as e:
        print(f"❌ Failed tagging {filename}: {e}")
