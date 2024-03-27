From python:3.11-slim

#  avoid delete buffer
 ENV PYTHONUNBUFFERED=1 

# avoid pip warning version
 ENV PIP_DISABLE_PIP_VERSION_CHECK=1

 WORKDIR /app

 COPY requirements.txt .

 RUN python -m venv venv
 RUN /bin/bash -c "source venv/bin/activate"

 RUN pip install -r requirements.txt

 COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

