FROM python:3.7-alpine
WORKDIR /mysite
ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip
RUN python3 -m pip install django
RUN pip3 install requests
EXPOSE 8000
COPY . .
CMD ["python3",  "manage.py", "runserver", "0.0.0.0:8000"]

