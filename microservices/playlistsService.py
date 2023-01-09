from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

playlistsService = Flask(__name__)
api = Api(playlistsService)
playlistsService.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/music-browser'
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
    trackConnection = db.relationship('TrackConnection',
                                      backref='trackConnection',
                                      lazy=True,
                                      cascade="delete, merge, save-update")


# db model of connection between playlist and tracks
class TrackConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, nullable=True)
    playlist_id = db.Column(db.ForeignKey('playlist.id'), nullable=False)


# fields for JSON
playlistFields = {
    'id': fields.Integer,
    'title': fields.String,
}

trackConnectionFields = {
    'id': fields.Integer,
    'track_id': fields.Integer,
    'playlist_id': fields.Integer
}


class PlaylistsEP(Resource):
    # get all playlists
    @marshal_with(playlistFields)
    def get(self):
        playlists = Playlist.query.all()
        return playlists

    # add new playlists
    @marshal_with(playlistFields)
    def post(self):
        data = request.json
        playlist = Playlist(title=data['title'])
        db.session.add(playlist)
        db.session.commit()
        return playlist


class PlaylistEP(Resource):
    # get playlist with given id
    @marshal_with(playlistFields)
    def get(self, playlist_id):
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        return playlist

    # update track with given id
    @marshal_with(playlistFields)
    def put(self, playlist_id):
        data = request.json
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        playlist.title = data['title']
        db.session.commit()
        return playlist

    # delete track with given id
    @marshal_with(playlistFields)
    def delete(self, playlist_id):
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        db.session.delete(playlist)
        db.session.commit()
        return playlist


class TrackConnectionsEP(Resource):
    # get all playlists
    @marshal_with(trackConnectionFields)
    def get(self):
        trackConnections = TrackConnection.query.all()
        return trackConnections

    # add new playlists
    @marshal_with(trackConnectionFields)
    def post(self):
        data = request.json
        trackConnection = TrackConnection(track_id=data['track_id'],
                                          playlist_id=data['playlist_id'])
        db.session.add(trackConnection)
        db.session.commit()
        return trackConnection


class TrackConnectionEP(Resource):
    # get track with given id
    @marshal_with(trackConnectionFields)
    def get(self, track_connection_id):
        trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
        return trackConnection

    # update track with given id
    @marshal_with(trackConnectionFields)
    def put(self, track_connection_id):
        data = request.json
        trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
        trackConnection.track_id = data['track_id']
        trackConnection.playlist_id = data['playlist_id']
        db.session.commit()
        return trackConnection

    # delete track with given id
    @marshal_with(trackConnectionFields)
    def delete(self, track_connection_id):
        trackConnection = TrackConnection.query.filter_by(id=track_connection_id).first()
        db.session.delete(trackConnection)
        db.session.commit()
        return trackConnection


class TracksInPlaylistEP(Resource):
    @marshal_with(trackConnectionFields)
    def get(self, playlist_id):
        tracks_in_playlist = TrackConnection.query.filter_by(playlist_id=playlist_id).all()
        return tracks_in_playlist


# endpoints
api.add_resource(PlaylistsEP, '/playlists')
api.add_resource(PlaylistEP, '/playlist/<int:playlist_id>')
api.add_resource(TrackConnectionsEP, '/track_connections')
api.add_resource(TrackConnectionEP, '/track_connection/<int:track_connection_id>')
api.add_resource(TracksInPlaylistEP, '/tracks_in_playlist/<int:playlist_id>')

if __name__ == '__main__':
    playlistsService.run(host="localhost", port=5001, debug=True)
