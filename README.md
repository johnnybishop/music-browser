# music-browser

## prequitites
- docker desktop
- python
- node js

## run database
```bash
docker-compose up -d
```

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
  pip install flask_restful
  pip install flask_sqlalchemy
  pip install psycopg2-binary
# run seach service from virtual env
  python microservices/tracksService.py
  python microservices/playlistsService.py
```
	