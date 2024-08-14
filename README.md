# Advanced RAG Workshop

Langauge
* [English](English)
* [한국어](한국어)


# English
## What is Advanced RAG Workshop?
> In this workshop, you'll understand several advanced RAG techniques and apply them to a multi-modal chatbot Q&A. This workshop aims to increase customer interest and engagement with AWS by introducing and practicing advanced Retrieval Augmented Generation (RAG) techniques that can be utilized in a real production environment, beyond the typical demo.

## Who need this workshop?
> No prior knowledge is required to perform this workshop.

This workshop is available to anyone who wants to:
* Acquire production-level RAG skills
* Increase technical understanding through hands-on practice
* Increase customer engagement with AWS services 

## How to deploy CDK stacks
```bash
git clone https://github.com/aws-samples/multi-modal-chatbot-with-advanced-rag.git
cd advanced-rag-workshop
npm i --save-dev @types/node
cdk bootstrap
cdk synth
cdk deploy --all --require-approval never
```

## Workshop Guide
You can see full workshop [here](https://catalog.us-east-1.prod.workshops.aws/workshops/a372f3ed-e99d-4c95-93b5-ee666375a387)

# 한국어

## Advnaced RAG Workshop이란?
이 워크샵에서는 여러 Advanced RAG 기법을 이해하고, Multi Modal 챗봇 Q&A에 여러 RAG 기법을 적용해 볼 수 있습니다. 일반적인 데모를 넘어 실제 프로덕션 환경에서 활용할 수 있는 고급 검색 증강 생성(RAG) 기술을 소개하고 실습함으로써 AWS에 대한 고객의 관심과 참여를 높이는 것을 목표로 합니다.

## 누구를 위한 워크샵 인가요?
> 이 워크샵을 수행하기 위해 별도의 사전 지식은 필요하지 않습니다.

다음 효과를 기대하는 모두가 이 워크샵을 사용할 수 있습니다:
* 프로덕션 수준의 RAG 기술 습득
* 실습을 통한 기술적 이해도 향상
* AWS 서비스 경험

## CDK 스택 배포 방법
```bash
git clone https://github.com/aws-samples/multi-modal-chatbot-with-advanced-rag.git
cd advanced-rag-workshop
npm i --save-dev @types/node
cdk bootstrap
cdk synth
cdk deploy --all --require-approval never
```

## 워크샵 가이드
이 [링크](https://catalog.us-east-1.prod.workshops.aws/workshops/a372f3ed-e99d-4c95-93b5-ee666375a387/ko-KR)에서 워크샵 콘텐츠를 확인할 수 있습니다
