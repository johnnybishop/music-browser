# music-browser

## prequitites
- docker desktop
- python

## run database
```bash
docker-compose up -d
```

## run python microservices
```python
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
	