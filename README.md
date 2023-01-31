# music-browser

Music browser is application created for browsing your personal music library. It was build with Python, Node JS and Vue JS. Backend was designed in microservices architecure with Docker support.

## prerequisites
- docker desktop
- python
- node js

## Run backend microservices
```bash 
# build api-gateway image
cd api-gateway
docker build . -t api_gateway

# build tracks service image 
cd ../microservices/tracks
docker build -t tracks_service .

# build playlists service image
cd ../playlists
docker image build -t playlists_service .

# run backend app
docker compose up -d
```

## Run frontend application
``` bash
cd client
npm install
npm run serve
```

# Local development
## run api gateway
```bash
# install dependencies
  npm i
# copy environment file
  cp .env.example .env
```
Set value of API_KEY environment variable.
```bash
# development mode
  npm run dev 
```

## run python microservices
```bash
# install virtualenv
  pip install virtualenv    
  virtualenv venv    
# run environment
  venv\Scripts\activate
# install dependencies for python services
  pip install flask
  pip install flask_api
  pip install flask_restful
  pip install flask_sqlalchemy
  pip install psycopg2-binary
# run seach service from virtual env
  python microservices/tracksService.py
  python microservices/playlistsService.py
```
	


