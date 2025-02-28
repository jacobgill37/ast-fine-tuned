import io
import os
import time
import urllib.request
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

planetrock_url = "http://stream-mz.planetradio.co.uk/planetrock.mp3?direct=true&aw_0_1st.playerid=BMUK_TuneIn&aw_0_1st.skey=7374499933"
kerrang_url = "https://edge-bauerall-01-gos2.sharp-stream.com/kerrang.mp3"
classic_fm_url = "https://ice-sov.musicradio.com/ClassicFMMP3"
capital_fm_url = "https://ice-sov.musicradio.com/CapitalUKMP3"

planetrock_path = "audio_files/planetrock/"
kerrang_path = "audio_files/kerrang/"
classic_fm_path = "audio_files/classic_fm/"
capital_fm_path = "audio_files/capital_fm/"

SNIPPET_DURATION = 5
LISTENING_TIME = 300

stations = {
    "planetrock": {"url": planetrock_url, "path": planetrock_path},
    "kerrang": {"url": kerrang_url, "path": kerrang_path},
    "classic_fm": {"url": classic_fm_url, "path": classic_fm_path},
    "capital_fm": {"url": capital_fm_url, "path": capital_fm_path},
}

for path in [planetrock_path, kerrang_path, classic_fm_path, capital_fm_path]:
    os.makedirs(path, exist_ok=True)


def save_snippets_of_audio(stream_url, duration):
    print(f"Downloading {duration} seconds of audio...")

    with urllib.request.urlopen(stream_url) as response:
        start_time = time.time()
        audio_data = b""
        while time.time() - start_time < duration:
            audio_data += response.read(1024)

    print("Download complete!")

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    duration_in_milliseconds = duration * 1000
    audio_snippet = audio_segment[:duration_in_milliseconds]
    return audio_snippet


def download_and_export_audio(url, path):
    audio = save_snippets_of_audio(url, SNIPPET_DURATION)
    audio.export(path, format="mp3")
    print(f"Exported audio to {path}")


time_to_listen_for = time.time() + LISTENING_TIME
print(f"Listening for {time_to_listen_for - time.time()} seconds...")

with ThreadPoolExecutor() as executor:
    while time.time() < time_to_listen_for:
        futures = []

        for station, data in stations.items():
            future = executor.submit(
                download_and_export_audio,
                data["url"],
                f"{data['path']}audio_{time.time()}.mp3",
            )
            futures.append(future)

        for future in futures:
            future.result()  # Wait for all futures to complete
