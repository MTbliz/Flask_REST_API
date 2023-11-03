from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db = SQLAlchemy()
db.init_app(app)


def api_resource(routes, **kwargs):
    def decorator(cls):
        api.add_resource(cls, *routes, **kwargs)
        return cls
    return decorator


def use_args(arg_list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parser = reqparse.RequestParser()
            for arg in arg_list:
                parser.add_argument(**arg)
                parsed_args = parser.parse_args()
            kwargs.update(parsed_args)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __init__(self, name, views, likes):
        self.name = name
        self.views = views
        self.likes = likes

    def __repr__(self):
        return f"Video(name = {self.name},views = {self.views}, likes = {self.likes})"

    @staticmethod
    def serialize():
        return {
            'id': fields.Integer,
            'name': fields.String,
            'views': fields.Integer,
            'likes': fields.Integer
        }


@api_resource(["/videos"])
class Videos(Resource):
    @marshal_with(VideoModel.serialize())
    def get(self):
        videos = VideoModel.query.all()
        return videos, 200


@api_resource(["/video", "/video/<int:video_id>"])
class Video(Resource):

    @marshal_with(VideoModel.serialize())
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Could not find video...")
        return video

    @marshal_with(VideoModel.serialize())
    @use_args([
        {'name': 'name', 'type': str, 'required': True, 'help': 'Name of the video'},
        {'name': 'views', 'type': int, 'required': True, 'help': 'Views of the video'},
        {'name': 'likes', 'type': int, 'required': True, 'help': 'Likes on the video'},
    ])
    def post(self, name, views, likes):

        video = VideoModel(name=name, views=views, likes=likes)
        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(video)
        db.session.commit()
        return '', 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)