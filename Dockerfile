FROM contraslash/alpine-django-deploy-common-with-pillow
# Those commands already are in finantic-base-build

RUN apk update
RUN apk add ffmpeg

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt


ADD . /code/

# I really don't need to make the migrations in this docker file
# RUN python manage.py makemigrations

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
