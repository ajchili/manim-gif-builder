from flask import Flask, send_file, request
import ffmpeg
from manim import *
import requests

app = Flask(__name__)

media_dir = "media"

@app.route("/")
def index():
	text = request.args.get('text', "boneless")
	font_size = int(request.args.get('fontSize', "24"))
	background_image = request.args.get('backgroundImage', None)

	scene = Scene()

	if (background_image is not None):
		r = requests.get(background_image)
		with open(f"{media_dir}/image.png", 'wb') as f:
			f.write(r.content)
		scene.add(ImageMobject(filename_or_array=f"{media_dir}/image.png"))
	
	scene.play(Write(Text(text=text, font_size=font_size)))
	scene.wait()
	scene.render(preview=False)

	stream = ffmpeg.input(scene.renderer.file_writer.movie_file_path)
	stream = ffmpeg.filter(stream, 'fps', fps=24, round='up')
	stream = ffmpeg.output(stream, f'{media_dir}/output.gif')
	ffmpeg.run(stream, overwrite_output=True)

	return send_file(f"{media_dir}/output.gif", download_name=f'{text}.gif')