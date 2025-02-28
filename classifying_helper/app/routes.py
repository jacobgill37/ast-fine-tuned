from flask import Blueprint, render_template, send_from_directory, redirect, url_for
import os
import shutil

bp = Blueprint("main", __name__)

audio_files = os.listdir(os.path.join(bp.root_path, "static", "audio"))
current_index = 0


@bp.route("/")
def index():
    global current_index
    if len(audio_files) == 0:
        return render_template("index.html", no_files=True)
    if current_index >= len(audio_files):
        current_index = 0
    audio_file = audio_files[current_index]
    return render_template("index.html", audio_file=audio_file, no_files=False)


@bp.route("/audio/<filename>")
def audio(filename):
    return send_from_directory(os.path.join(bp.root_path, "static", "audio"), filename)


@bp.route("/classify/<category>/<filename>", methods=["POST"])
def classify(category, filename):
    global current_index
    # Define the source and destination paths
    src_path = os.path.join(bp.root_path, "static", "audio", filename)
    dest_dir = os.path.join(
        bp.root_path, "..", "..", "dataset_5_seconds", "train", category
    )
    dest_path = os.path.join(dest_dir, filename)

    # Create the category directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Move the file to the category folder
    shutil.move(src_path, dest_path)

    # Update the audio files list and current index
    audio_files.remove(filename)
    current_index += 1

    return redirect(url_for("main.index"))
