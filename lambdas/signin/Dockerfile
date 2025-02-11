FROM public.ecr.aws/lambda/python:3.13

RUN pip3 install --upgrade pip

COPY ./requirements.txt ./

RUN python3.13 -m pip install -r requirements.txt -t .

COPY . .

CMD ["main.lambda_handler"]