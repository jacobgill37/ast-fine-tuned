import io
import time
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor

import urllib.request

planetrock_url = "http://stream-mz.planetradio.co.uk/planetrock.mp3?direct=true&aw_0_1st.playerid=BMUK_TuneIn&aw_0_1st.skey=7374499933"
kerrang_url = "https://edge-bauerall-01-gos2.sharp-stream.com/kerrang.mp3"
classic_fm_url = "https://ice-sov.musicradio.com/ClassicFMMP3"

planetrock_path = "audio_files/planetrock/"
kerrang_path = "audio_files/kerrang/"
classic_fm_path = "audio_files/classic_fm/"


def save_30_seconds_of_audio(stream_url):
    print("Downloading 30 seconds of audio...")
    with urllib.request.urlopen(stream_url) as response:
        start_time = time.time()
        audio_data = b""
        while time.time() - start_time < 30:
            audio_data += response.read(1024)

    print("Download complete!")

    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    thirty_seconds_audio = audio_segment[:30000]  # 30 seconds in milliseconds
    return thirty_seconds_audio


def download_and_export_audio(url, path):
    audio = save_30_seconds_of_audio(url)
    audio.export(path, format="mp3")
    print(f"Exported audio to {path}")


ten_minutes_from_now = time.time() + 600

with ThreadPoolExecutor() as executor:
    while time.time() < ten_minutes_from_now:
        futures = [
            executor.submit(
                download_and_export_audio,
                planetrock_url,
                f"{planetrock_path}audio_{time.time()}.mp3",
            ),
            executor.submit(
                download_and_export_audio,
                kerrang_url,
                f"{kerrang_path}audio_{time.time()}.mp3",
            ),
            executor.submit(
                download_and_export_audio,
                classic_fm_url,
                f"{classic_fm_path}audio_{time.time()}.mp3",
            ),
        ]

        for future in futures:
            future.result()  # Wait for all futures to complete
