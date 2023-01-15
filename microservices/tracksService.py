from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from datetime import datetime

tracksService = Flask(__name__)
api = Api(tracksService)

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
    createdAt = db.Column(db.String, nullable=False)


# fields for JSON
trackFields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'track_url': fields.String,
    'createdAt': fields.String
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
            if ('title' in data) & ('author' in data) & ('track_url' in data):
                track = Track(title=data['title'],
                              author=data['author'],
                              track_url=data['track_url'],
                              createdAt=str(datetime.now())[:-7])
                db.session.add(track)
                db.session.commit()
                return track
            else:
                return abort(400, 'Received JSON data is incorrect!')
        else:
            return abort(400, 'Provide correct api key!')


class TrackEP(Resource):
    # get track with given id
    @marshal_with(trackFields)
    def get(self, track_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            track = Track.query.filter_by(id=track_id).first()
            if track:
                return track
            else:
                return abort(400, f'Track with id {track_id} does not exist!')
        else:
            return abort(400, 'Provide correct api key!')

    # update track with given id
    @marshal_with(trackFields)
    def put(self, track_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            if ('title' in data) & ('author' in data) & ('track_url' in data):
                track = Track.query.filter_by(id=track_id).first()
                if track:
                    track.title = data['title']
                    track.author = data['author']
                    track.track_url = data['track_url']
                    db.session.commit()
                    return track
                else:
                    return abort(400, f'Track with id {track_id} does not exist!')
            else:
                return abort(400, 'Received JSON data is incorrect!')
        else:
            return abort(400, 'Provide correct api key!')

    # delete track with given id
    @marshal_with(trackFields)
    def delete(self, track_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            track = Track.query.filter_by(id=track_id).first()
            if track:
                db.session.delete(track)
                db.session.commit()
                return track
            else:
                return abort(400, f'Track with id {track_id} does not exist!')
        else:
            return abort(400, 'Provide correct api key!')


api.add_resource(TracksEP, '/tracks')
api.add_resource(TrackEP, '/track/<int:track_id>')

if __name__ == '__main__':
    tracksService.run(host="localhost", port=5000, debug=True)
