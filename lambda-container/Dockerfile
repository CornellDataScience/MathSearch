FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN yum -y update
RUN yum -y install mesa-libGL

# Install the specified packages
RUN pip install -r requirements.txt

# Copy lambda function code and the OCR models
COPY ocr-models ${LAMBDA_TASK_ROOT}/ocr-models
COPY constants.py ${LAMBDA_TASK_ROOT}
COPY dataHandler.py ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]