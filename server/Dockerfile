# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.6.3
COPY . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]