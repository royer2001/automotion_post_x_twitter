from .. import db
from datetime import datetime

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    images = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"<Post {self.id}>"
