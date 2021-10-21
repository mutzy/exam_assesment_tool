from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
import resources


app = Flask(__name__)

app.debug = True
app.env = 'Development'
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/omr_procs/',methods=['GET','POST'])
def omr_proc_page():
	if request.method == "POST" and request.files['file'].filename != '':
		f = request.files['file']
		filename = secure_filename(f.filename)
		d = os.path.join(app.config['UPLOAD_FOLDER'],filename)
		f.save(d)
		scor = resources.omr_proc(f.filename)
		cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'],'result.png'),scor)
		res = os.path.join(app.config['UPLOAD_FOLDER'],'result.png')
		return render_template('index.html',score=scor, disp=res)
	return render_template('index.html',score='')

if __name__ == "__main__":
	app.run()