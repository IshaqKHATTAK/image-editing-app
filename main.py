from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg','webp'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def preprocessing(filename, operation):
    print(f'the filename is {filename} and the operation is {operation}')
    image = cv2.imread(f'uploads/{filename}')
    match operation:
        case 'cgray':
            process = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f'static/{filename}', process)
    
@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/edit", methods = ['GET','POST'])
def edit():
    operation = request.form.get('operation') #to get the kind of operation from the form on index.html
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('error.html')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('error.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            preprocessing(filename, operation)
            return render_template('index.html')

app.run(debug=True)