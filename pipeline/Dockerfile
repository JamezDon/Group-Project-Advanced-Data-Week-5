FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract.py .
COPY load.py .
COPY pipeline_lambda.py .

CMD ["pipeline_lambda.lambda_handler"]