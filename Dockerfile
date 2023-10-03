#imagen python.
FROM python:3.9-alpine

#Copia el directorio del contenedor.
COPY . /SQL_ALCHEMY
WORKDIR /SQL_ALCHEMY
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#expone el puerto del contenedor
EXPOSE 5005
# RUN chmod +x /sql-alchemy
#ENTRYPOINT ["python3"]

ENV FLASK_APP=app/__init__.py
ENV key=value

CMD ["sh", "run.sh"]
#CMD [ "flask", "run","--host=0.0.0.0","--port=5005"]