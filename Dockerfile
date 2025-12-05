FROM python:3

WORKDIR /usr/src/app 

# ./ points to the working directory
COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt

# WILL COPY THE WHOLE DIRECTORY INSIDE THE WORKDIR  WE NEED .dockerignore
COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
