FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/app
# Environment Variables
ENV OVERRIDE_S3_ENDPOINT=http://127.0.0.1:9000/
ENV SOURCE_BUCKET=dataENVs
ENV SOURCE_PATH=s3://dataENVs/csv_data/stark_doc_data.csv
ENV access=minioadmin
ENV secret=minioadmin
ENV region=ap-south-1
ENV REDIS_ENDPOINT=redis://localhost:6379
ENV RESUME_SOURCE_PATH=s3://datasets/csv_data/resume_data.csv
ENV RESUME_BUCKET=resumes

COPY requirementslin.txt .

RUN pip3 --no-cache-dir install --upgrade pip

RUN pip3 install --no-cache-dir -r requirementslin.txt


COPY . /home/app
WORKDIR /home/app

EXPOSE 5001
CMD chmod +x run.sh
CMD ["sh", "run.sh"]
