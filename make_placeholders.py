from pydub import AudioSegment
import os

def make_placeholders():
    os.makedirs("static/episodes", exist_ok=True)
    shows = ["bop", "wlb"]

    for show in shows:
        for i in range(1, 4):
            filename = f"static/episodes/{show}-ep{i}.mp3"
            if not os.path.exists(filename):
                silence = AudioSegment.silent(duration=5000)  # 5 sec silence
                silence.export(filename, format="mp3")
                print(f"Created {filename}")
            else:
                print(f"Skipped {filename} (already exists)")

if __name__ == "__main__":
    make_placeholders()
    print("✅ Placeholder MP3s ready in static/episodes/")
