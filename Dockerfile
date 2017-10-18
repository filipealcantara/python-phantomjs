FROM python:3-onbuild
COPY hkn_env /etc/
CMD [ "python", "./app.py" ]
EXPOSE 5000
