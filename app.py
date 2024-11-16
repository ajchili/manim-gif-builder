from flask import Flask, send_file, request
import ffmpeg
from manim import *
import requests
import os
import urllib.parse

app = Flask(__name__)

media_dir = "media"

@app.route("/")
def index():
	text = request.args.get('text', "boneless")
	if text.endswith(".gif"):
		text = text[0:-4] or "boneless"

	font_size = int(request.args.get('fontSize', "24"))
	background_image = request.args.get('backgroundImage', None)
	# Account for issue with DNS masking redirects replacing "//" with "/" in image urls (e.g. "https://" -> "https:/")
	if background_image != None and ":/" in background_image and "://" not in background_image:
		background_image = background_image.replace(":/", "://")

	image_hash = urllib.parse.quote_plus(f"{text}_{str(font_size)}_{str(background_image)}")
	output_path = f"{media_dir}/{image_hash}.gif"

	scene = Scene()

	if not os.path.exists(f'{media_dir}/{image_hash}.gif'):
		if (background_image is not None):
			r = requests.get(background_image)
			with open(f"{media_dir}/image.png", 'wb') as f:
				f.write(r.content)
			scene.add(ImageMobject(filename_or_array=f"{media_dir}/image.png"))
		
		scene.play(Write(Text(text=text, font_size=font_size, font="Times New Roman")))
		scene.wait()
		scene.render(preview=False)

		stream = ffmpeg.input(scene.renderer.file_writer.movie_file_path)
		stream = ffmpeg.filter(stream, 'fps', fps=24, round='up')
		stream = ffmpeg.filter(stream, 'scale', 1280, -1)
		stream = ffmpeg.output(stream,output_path)
		ffmpeg.run(stream, overwrite_output=True)

	return send_file(output_path, download_name=f'{text}.gif')