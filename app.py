from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
db = SQLAlchemy(app)

# Enable CORS for all routes
CORS(app)

# Bug Model
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    severity = db.Column(db.String(20))
    reported_by = db.Column(db.String(50))
    date_reported = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Bug {self.title}>'

# Create all database tables
with app.app_context():
    db.create_all()

# Cute messages for celebrations
CELEBRATION_MESSAGES = [
    "🎉 Woohoo! We've squashed 100 bugs together! Time for a party! 🎈",
    "🦋 Another century of bugs caught! You're all amazing! 🌟",
    "🐞 100 bugs down! Let's celebrate with cake! 🍰",
    "🎮 Level up! 100 bugs fixed - you're all debugging heroes! 👑",
    "🌈 Century milestone reached! Group hug time! 🤗"
]

@app.route('/')
def index():
    bugs = Bug.query.order_by(Bug.date_reported.desc()).all()
    total_bugs = len(bugs)
    show_celebration = total_bugs > 0 and total_bugs % 100 == 0

    if show_celebration:
        celebration_message = random.choice(CELEBRATION_MESSAGES)
    else:
        celebration_message = None

    return render_template('index.html', 
                           bugs=bugs, 
                           total_bugs=total_bugs,
                           show_celebration=show_celebration,
                           celebration_message=celebration_message)

@app.route('/add_bug', methods=['POST'])
def add_bug():
    title = request.form['title']
    description = request.form['description']
    severity = request.form['severity']
    reported_by = request.form['reported_by']

    new_bug = Bug(
        title=title,
        description=description,
        severity=severity,
        reported_by=reported_by
    )

    db.session.add(new_bug)
    db.session.commit()

    return jsonify({'message': 'Bug reported successfully!'}), 201  # Return JSON

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    bug = Bug.query.get_or_404(id)
    bug.status = 'Closed' if bug.status == 'Open' else 'Open'
    db.session.commit()
    return redirect(url_for('index'))

# New API endpoint to get all bugs
@app.route('/api/bugs', methods=['GET'])
def get_bugs():
    bugs = Bug.query.order_by(Bug.date_reported.desc()).all()
    return jsonify({
        'bugs': [
            {
                'id': bug.id,
                'title': bug.title,
                'description': bug.description,
                'status': bug.status,
                'severity': bug.severity,
                'reported_by': bug.reported_by,
                'date_reported': bug.date_reported.strftime("%Y-%m-%d %H:%M:%S")
            }
            for bug in bugs
        ]
    })

# New API endpoint to delete a bug
@app.route('/delete_bug/<int:id>', methods=['DELETE'])
def delete_bug(id):
    bug = Bug.query.get_or_404(id)
    db.session.delete(bug)
    db.session.commit()
    return jsonify({'message': 'Bug deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
