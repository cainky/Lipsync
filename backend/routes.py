import os
from flask import jsonify, request, Response
from pathlib import Path
from services.merge_service import merge_audio_video
from utils import get_uploads_dir

ALLOWED_EXTENSIONS = {"mp4", "wav", "webm"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def init_app(app):
    @app.route("/uploads/<filename>", methods=["GET"])
    def uploaded_file(filename):
        uploads_dir = get_uploads_dir()
        filepath = os.path.join(uploads_dir, filename)

        try:
            with open(filepath, "rb") as f:
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
                return jsonify(error=str(e)), 500
        return jsonify(error="File type not allowed"), 400
