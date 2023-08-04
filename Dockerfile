FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./translation translation/
COPY lambda_function.py lambda_function.py

CMD [ "lambda_function.lambda_handler" ]
