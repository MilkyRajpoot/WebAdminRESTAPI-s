
#!/bin/bash

# Start Gunicorn processes

ALL ALL: NO Password
source venv/bin/activate
echo Starting Gunicorn.

wget --retry-connrefused --waitretry=2 --tries=2 http://127.0.0.1:8000/api/vimeo/job/ && exec gunicorn School.wsgi:application --timeout 3600 --workers=8 --threads 8 &

sudo fuser -k 8000/tcp
#wget http://127.0.0.1:8000/api/vimeo/job/
sudo systemctl restart gunicorn
exit 1