import os
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, APIC, error
from mutagen.mp3 import MP3
from mutagen.oggopus import OggOpus
from mutagen.flac import FLAC
from mutagen.mp4 import MP4, MP4Cover

AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.flac', '.opus']
ARTIST = "Varun"
ALBUM = "WebVPlayer OST"
GENRE = "Varun Vibes"
COVER_IMAGE_PATH = "my_art.png"

def tag_mp3(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass
        audio["TIT2"] = TIT2(encoding=3, text=os.path.splitext(os.path.basename(file_path))[0])
        audio["TPE1"] = TPE1(encoding=3, text=ARTIST)
        audio["TALB"] = TALB(encoding=3, text=ALBUM)
        audio["TCON"] = TCON(encoding=3, text=GENRE)

        with open(COVER_IMAGE_PATH, 'rb') as albumart:
            audio["APIC"] = APIC(
                encoding=3,
                mime='image/png',
                type=3,  # Cover (front)
                desc=u'Cover',
                data=albumart.read()
            )

        audio.save()
        return True
    except Exception as e:
        return False

def tag_opus(file_path):
    try:
        audio = OggOpus(file_path)
        audio['title'] = os.path.splitext(os.path.basename(file_path))[0]
        audio['artist'] = ARTIST
        audio['album'] = ALBUM
        audio['genre'] = GENRE
        audio.save()
        return True
    except Exception as e:
        return False

def tag_flac(file_path):
    try:
        audio = FLAC(file_path)
        audio['title'] = os.path.splitext(os.path.basename(file_path))[0]
        audio['artist'] = ARTIST
        audio['album'] = ALBUM
        audio['genre'] = GENRE
        with open(COVER_IMAGE_PATH, 'rb') as img:
            audio.add_picture(img.read())
        audio.save()
        return True
    except Exception as e:
        return False

def tag_m4a(file_path):
    try:
        audio = MP4(file_path)
        audio["\xa9nam"] = [os.path.splitext(os.path.basename(file_path))[0]]
        audio["\xa9ART"] = [ARTIST]
        audio["\xa9alb"] = [ALBUM]
        audio["\xa9gen"] = [GENRE]
        with open(COVER_IMAGE_PATH, 'rb') as albumart:
            audio["covr"] = [MP4Cover(albumart.read(), imageformat=MP4Cover.FORMAT_PNG)]
        audio.save()
        return True
    except Exception as e:
        return False

taggers = {
    '.mp3': tag_mp3,
    '.opus': tag_opus,
    '.flac': tag_flac,
    '.m4a': tag_m4a
}

# === MAIN LOOP ===
for filename in os.listdir('.'):
    _, ext = os.path.splitext(filename)
    if ext.lower() in taggers:
        print(f"Tagging: {filename}")
        if taggers[ext.lower()](filename):
            print("✅ Done")
        else:
            print("❌ Failed")
