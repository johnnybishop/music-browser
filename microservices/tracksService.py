from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask import abort

import os

tracksService = Flask(__name__)
api = Api(tracksService)

'''
tracksService.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracksDB.db'
tracksService.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(tracksService)
'''

tracksService.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/music-browser'
tracksService.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(tracksService)


# create test db
@tracksService.route('/init/')
def init():
    with tracksService.app_context():
        db.create_all()
    return 'database has been initialized'


# db model
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    track_url = db.Column(db.String, nullable=False)


# fields for JSON
trackFields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'track_url': fields.String
}


class TracksEP(Resource):
    # get all tracks
    @marshal_with(trackFields)
    def get(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            all_tracks = Track.query.all()
            return all_tracks
        else:
            return abort(400, 'Provide correct api key!')

    # add new track
    @marshal_with(trackFields)
    def post(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            track = Track(title=data['title'],
                          author=data['author'],
                          track_url=data['track_url'])
            db.session.add(track)
            db.session.commit()
            return track
        else:
            return abort(400, 'Provide correct api key!')


class TrackEP(Resource):
    # get track with given id
    @marshal_with(trackFields)
    def get(self, video_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            track = Track.query.filter_by(id=video_id).first()
            return track
        else:
            return abort(400, 'Provide correct api key!')

    # update track with given id
    @marshal_with(trackFields)
    def put(self, video_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            track = Track.query.filter_by(id=video_id).first()
            track.title = data['title']
            track.author = data['author']
            track.track_url = data['track_url']
            db.session.commit()
            return track
        else:
            return abort(400, 'Provide correct api key!')

    # delete track with given id
    @marshal_with(trackFields)
    def delete(self, video_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            track = Track.query.filter_by(id=video_id).first()
            db.session.delete(track)
            db.session.commit()
            return track, 200
        else:
            return abort(400, 'Provide correct api key!')


api.add_resource(TracksEP, '/tracks')
api.add_resource(TrackEP, '/track/<int:video_id>')

if __name__ == '__main__':
    tracksService.run(host="localhost", port=5000, debug=True)
