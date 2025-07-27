from mutagen import File
import os

missing_art = []

for filename in os.listdir():
    if filename.endswith(('.mp3', '.opus')):
        audio = File(filename)
        if filename.endswith('.mp3'):
            # Check for album art in MP3
            if not audio.tags or not any(tag.startswith('APIC') for tag in audio.tags.keys()):
                missing_art.append(filename)
        elif filename.endswith('.opus'):
            # Check for album art in Opus
            if not audio or 'metadata_block_picture' not in audio:
                missing_art.append(filename)

print("❌ Files without album art:")
for f in missing_art:
    print(f)
