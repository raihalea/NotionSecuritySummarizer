FROM public.ecr.aws/lambda/python:3.13-arm64

# 必要なライブラリをインストール
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Lambda関数コードをコピー
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Lambdaエントリポイント
CMD ["lambda_function.lambda_handler"]