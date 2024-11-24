from flask import Flask, render_template, request, redirect, url_for
from models import db, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)


@app.route('/note/<int:id>')
def note(id):
    note = Note.query.get(id)
    if not note:
        return "Nota não encontrada!", 404
    return render_template('note.html', note=note)


@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_note.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
