import os, logging
from flask import jsonify, request, Response, current_app
from pathlib import Path
from services.merge_service import merge_audio_video
from utils import get_uploads_dir, get_full_path
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"mp4", "wav", "webm"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def init_app(app):
    @app.route("/uploads/<filename>", methods=["GET"])
    def uploaded_file(filename):
        filename = secure_filename(filename)
        uploads_dir = get_uploads_dir(current_app.config)
        fullpath = get_full_path(uploads_dir, filename)

        if not fullpath.startswith(uploads_dir):
            return jsonify(error="Access denied"), 403

        try:
            with open(fullpath, "rb") as f:
                file_content = f.read()
            return Response(file_content, content_type="video/webm")
        except FileNotFoundError:
            return jsonify(error="File not found"), 404

    @app.route("/api/merge", methods=["POST"])
    def merge():
        if "audio" not in request.files or "video" not in request.files:
            return jsonify(error="Missing audio or video file"), 400

        audio_file = request.files["audio"]
        video_file = request.files["video"]

        if audio_file.filename == "" or video_file.filename == "":
            return jsonify(error="No selected file"), 400

        if (
            audio_file
            and allowed_file(audio_file.filename)
            and video_file
            and allowed_file(video_file.filename)
        ):
            try:
                video_path = merge_audio_video(audio_file, video_file)
                if Path(video_path).is_file():
                    output_path = "/uploads/" + os.path.basename(video_path)
                    return (
                        jsonify(videoPath=output_path),
                        200,
                    )
                else:
                    return (
                        jsonify(error="Output file not found."),
                        404,
                    )
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                return jsonify(error=f"An internal error has occurred!"), 500
        return jsonify(error="File type not allowed"), 400
