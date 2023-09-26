FROM python:3.9

#copia el directorio del contenedor
COPY ./ SQL_ALCHEMY
WORKDIR /SQL_ALCHEMY
RUN pip install -r requeriments.txt

#EXPONE EL PUERTO 5000 DEL CONTENEDOR 
EXPOSE 5005

ENTRYPOINT [ "python3" ]

CMD [ "__init__.py" ]