import os
import tempfile
from flask import Flask, request, redirect, url_for, render_template
import whisper


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            # Save the uploaded file to a temporary directory
            filename = os.path.join(tempfile.gettempdir(), file.filename)
            file.save(filename)
            # Load the transcription model and transcribe the audio file
            model = whisper.load_model("base")
            result = model.transcribe(filename)
            # Render the transcription result on a separate page
            return redirect(url_for("result", text=result["text"]))
    return render_template("index.html")


@app.route("/result")
def result():
    text = request.args.get("text")
    return render_template("result.html", text=text)


if __name__ == "__main__":
    app.run(debug=True)
