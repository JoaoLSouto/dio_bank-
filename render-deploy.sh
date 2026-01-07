set - 
poetry run flask --app src.app db upgrade
poetry run gunicorn src.wgsi:app