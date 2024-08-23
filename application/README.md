# How to run this application

> If you clone this repo and run 'cdk deploy', you don't need to run it yourself.

## Structure

1. `bedrock.py`

- Amazon Bedrock 및 Reranker, Hybrid search, parent-document 등의 RAG 기술 구현 파일

2. `streamlit.py`

- 애플리케이션의 front-end 파일, 실행 시 `bedrock.py`을 import해서 사용

## Start
1. web_ui 폴더 접근
```
cd multi-modal-chatbot-with-advanced-rag/application
```

2. Python 종속 라이브러리 설치

```
pip install -r requirements.txt
```

3. Streamlit 애플리케이션 작동

```
streamlit run streamlit.py --server.port 8080
```

3. 접속하기

- Streamlit 작동 시 표시되는 External link 혹은 EC2 public ip로 접속
