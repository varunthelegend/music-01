import os
from mutagen import File
from mutagen.id3 import APIC, TIT2, TPE1, TALB, TCON
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import Picture, FLAC

AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.flac', '.opus')
COVER_PATH = "my_art.png"

def tag_audio(file_path):
    print(f"Tagging: {file_path}")
    audio = File(file_path, easy=False)

    if not audio:
        print("❌ Unsupported file or error")
        return

    title = os.path.splitext(os.path.basename(file_path))[0]
    artist = "Varun"
    album = "WebVPlayer OST"
    genre = "Varun Vibes"

    try:
        if file_path.endswith(".mp3"):
            audio["TIT2"] = TIT2(encoding=3, text=title)
            audio["TPE1"] = TPE1(encoding=3, text=artist)
            audio["TALB"] = TALB(encoding=3, text=album)
            audio["TCON"] = TCON(encoding=3, text=genre)
            with open(COVER_PATH, 'rb') as img:
                audio["APIC"] = APIC(encoding=3, mime='image/png', type=3, desc=u'Cover', data=img.read())
            audio.save()
        
        elif file_path.endswith(".m4a"):
            audio["\xa9nam"] = title
            audio["\xa9ART"] = artist
            audio["\xa9alb"] = album
            audio["\xa9gen"] = genre
            with open(COVER_PATH, 'rb') as img:
                audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_PNG)]
            audio.save()
        
        elif file_path.endswith(".flac"):
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio["genre"] = genre
            pic = Picture()
            with open(COVER_PATH, 'rb') as img:
                pic.data = img.read()
            pic.type = 3
            pic.mime = "image/png"
            audio.add_picture(pic)
            audio.save()
        
        elif file_path.endswith(".opus"):
            audio["title"] = [title]
            audio["artist"] = [artist]
            audio["album"] = [album]
            audio["genre"] = [genre]
            # Opus doesn't fully support embedded album art in many players.
            audio.save()
        
        else:
            print("❌ Not a supported format")

        print("✅ Done")

    except Exception as e:
        print(f"⚠️ Error tagging {file_path}: {e}")

def tag_all():
    for fname in os.listdir("."):
        if fname.lower().endswith(AUDIO_EXTENSIONS):
            tag_audio(fname)

if __name__ == "__main__":
    tag_all()
