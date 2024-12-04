FROM python:3.10

WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app /code/app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Start FastAPI on the same port that we expose
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
