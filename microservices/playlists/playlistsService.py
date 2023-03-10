from flask import Flask, request, jsonify
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy
from flask import abort
from datetime import datetime
from flask_api import status


playlistsService = Flask(__name__)
api = Api(playlistsService)
playlistsService.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@db:5432/music-browser'
playlistsService.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(playlistsService)


# create test db
@playlistsService.route('/init/')
def init():
    with playlistsService.app_context():
        db.create_all()
    return 'database has been initialized'


# db playlist model
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.String, nullable=False)
    trackConnection = db.relationship('TrackConnection',
                                      backref='trackConnection',
                                      lazy=True,
                                      cascade="delete, merge, save-update")

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    track_url = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.String, nullable=False)


# db model of connection between playlist and tracks
class TrackConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, nullable=True)
    playlist_id = db.Column(db.ForeignKey('playlist.id'), nullable=False)


# fields for JSON
playlistFields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'createdAt': fields.String,
    'track_ids': fields.List(fields.Integer)
}

trackConnectionFields = {
    'id': fields.Integer,
    'track_id': fields.Integer,
    'playlist_id': fields.Integer
}


class PlaylistsEP(Resource):
    # get all playlists
    def get(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            playlists = Playlist.query.order_by(Playlist.createdAt.desc()).all()
            extended_playlists = []
            for playlist in playlists:
                playlist = dict(playlist.__dict__)
                del playlist['_sa_instance_state']
                tracks_in_playlist = TrackConnection.query.filter_by(playlist_id=playlist['id']).all()
                tracks = []
                for track_in_playlist in tracks_in_playlist:
                    track_id = track_in_playlist.id
                    track = Track.query.filter_by(id=track_id).first()
                    track = dict(track.__dict__)
                    del track['_sa_instance_state']
                    tracks.append(track)
                playlist['tracks'] = tracks
                extended_playlists.append(playlist)
            return extended_playlists
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # add new playlists
    def post(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            if ('title' in data) & ('description' in data):
                playlist = Playlist(title=data['title'],
                                    description=data['description'],
                                    createdAt=str(datetime.now())[:-7])
                db.session.add(playlist)
                db.session.commit()
                return playlist.id
            else:
                return abort(jsonify(message='Received JSON data is incorrect',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))


class PlaylistEP(Resource):
    # get playlist with given id
    def get(self, playlist_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            playlist = Playlist.query.filter_by(id=playlist_id).first()
            if playlist:
                playlist = dict(playlist.__dict__)
                del playlist['_sa_instance_state']
                tracks_in_playlist = TrackConnection.query.filter_by(playlist_id=playlist_id).all()
                tracks = []
                for track_in_playlist in tracks_in_playlist:
                    track_id = track_in_playlist.id
                    track = Track.query.filter_by(id=track_id).first()
                    track = dict(track.__dict__)
                    del track['_sa_instance_state']
                    tracks.append(track)
                playlist['tracks'] = tracks
                return playlist
            else:
                return abort(jsonify(message=f'Playlist with id {playlist_id} does not exist!',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # update track with given id
    def put(self, playlist_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            if ('title' in data) & ('description' in data):
                playlist = Playlist.query.filter_by(id=playlist_id).first()
                if playlist:
                    playlist.title = data['title']
                    playlist.description = data['description']
                    db.session.commit()
                    return status.HTTP_200_OK
                else:
                    return abort(jsonify(message=f'Playlist with id {playlist_id} does not exist!',
                                         error_code=404))
            else:
                return abort(jsonify(message='Received JSON data is incorrect',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # delete track with given id
    def delete(self, playlist_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            playlist = Playlist.query.filter_by(id=playlist_id).first()
            if playlist:
                db.session.delete(playlist)
                db.session.commit()
                return status.HTTP_200_OK
            else:
                return abort(jsonify(message=f'Playlist with id {playlist_id} does not exist!',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))


class TrackConnectionsEP(Resource):
    # get all playlists
    @marshal_with(trackConnectionFields)
    def get(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            trackConnections = TrackConnection.query.all()
            return trackConnections
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # add new playlists
    def post(self):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            if ('track_id' in data) & ('playlist_id' in data):
                trackConnection = TrackConnection(track_id=data['track_id'],
                                                  playlist_id=data['playlist_id'])
                db.session.add(trackConnection)
                db.session.commit()
                return status.HTTP_200_OK
            else:
                return abort(jsonify(message='Received JSON data is incorrect',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))


class TrackConnectionEP(Resource):
    # get track with given id
    @marshal_with(trackConnectionFields)
    def get(self, track_connection_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
            if trackConnection:
                return trackConnection
            else:
                return abort(jsonify(message=f'Track connection with id {track_connection_id} does not exist!',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # update track with given id
    def put(self, track_connection_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            data = request.json
            if ('track_id' in data) & ('playlist_id' in data):
                trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
                if trackConnection:
                    trackConnection.track_id = data['track_id']
                    trackConnection.playlist_id = data['playlist_id']
                    db.session.commit()
                    return status.HTTP_200_OK
                else:
                    return abort(jsonify(message=f'Track connection with id {track_connection_id} does not exist!',
                                         error_code=404))
            else:
                return abort(jsonify(message='Received JSON data is incorrect',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))

    # delete track with given id
    def delete(self, track_connection_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
            if trackConnection:
                db.session.delete(trackConnection)
                db.session.commit()
                return status.HTTP_200_OK
            else:
                return abort(jsonify(message=f'Track connection with id {track_connection_id} does not exist!',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))


class TracksInPlaylistEP(Resource):
    @marshal_with(trackConnectionFields)
    def get(self, playlist_id):
        headers = request.headers
        auth = headers.get("apiKey")
        if auth == '6327cc80-3093-4beb-90ee-191d69076366':
            if Playlist.query.filter_by(id=playlist_id).first():
                tracks_in_playlist = TrackConnection.query.filter_by(playlist_id=playlist_id).all()
                return tracks_in_playlist
            else:
                return abort(jsonify(message=f'Playlist with id {playlist_id} does not exist!',
                                     error_code=404))
        else:
            return abort(jsonify(message='Provide correct api key!',
                                 error_code=404))


# endpoints
api.add_resource(PlaylistsEP, '/playlist')
api.add_resource(PlaylistEP, '/playlist/<int:playlist_id>')
api.add_resource(TrackConnectionsEP, '/track_connection')
api.add_resource(TrackConnectionEP, '/track_connection/<int:track_connection_id>')
api.add_resource(TracksInPlaylistEP, '/tracks_in_playlist/<int:playlist_id>')

if __name__ == '__main__':
    # setup for local develpoment
    # playlistsService.run(host="localhost", port=5001, debug=True)
    
    # setup for docker deployment
    playlistsService.run(host="0.0.0.0", port=5001, debug=True)
