from mic.extensions import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.character_id
