FROM python:3.6-onbuild 
EXPOSE 8000
CMD ["/usr/local/bin/python", "keepmealive/manage.py", "runserver", "0.0.0.0:8000"]