FROM python:3.6-onbuild 
EXPOSE 8000
CMD ["/usr/local/bin/gunicorn", "-w 2", "-b 0.0.0.0:8000", "wsgi:application", "--reload"]

