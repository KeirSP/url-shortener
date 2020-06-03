from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class URLtable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<URL: %r>' % self.id


def init_db():
    """For use on command line for setting up
    the database.
    """

    db.drop_all()
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        new_url = URLtable(url=original_url)
        print(original_url)
        try:
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for('getNewURL', newURL = original_url))
        except:
            return 'There was an issue adding your url'
    else:
        return render_template('index.html')


@app.route('/newURL/<newURL>', methods=["GET"])
def getNewURL(newURL):
        urls = URLtable.query.filter_by(url=newURL).first()
        return render_template('returnURL.html', url=urls)

@app.route('/<uid>', methods=["GET"])
def teleport(uid):
    redirectedurl = URLtable.query.filter_by(id=uid).first()
    return redirect('http://' + redirectedurl.url)