#!/bin/bash

set -e


sudo -u ec2-user -i <<'EOF'
 
#source /home/ec2-user/anaconda3/bin/deactivate
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pip
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U awscli==1.33.16
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U botocore==1.34.134
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U boto3==1.34.134
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U sagemaker==2.224.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U langchain==0.2.6
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U langchain-community==0.2.6
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U langchain_aws==0.1.8
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U termcolor==2.4.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U transformers==4.41.2
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U librosa==0.10.2.post1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U opensearch-py==2.6.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U sqlalchemy #==2.0.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pypdf==4.2.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U ipython==8.25.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U ipywidgets==8.1.3
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U anthropic==0.30.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U faiss-cpu==1.8.0.post1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U jq==1.7.0
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pydantic==2.7.4

sudo rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
sudo yum -y update
sudo yum install -y poppler-utils
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U lxml==5.2.2
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U kaleido==0.2.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U uvicorn==0.30.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pandas==2.2.2
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U numexpr==2.10.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pdf2image==1.17.0

sudo amazon-linux-extras install libreoffice -y
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U "unstructured[all-docs]==0.13.2"

/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U python-dotenv==1.0.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U llama-parse==0.4.4
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U pymupdf==1.24.7

# Uninstall nltk 3.8.2 and install 3.8.1
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip uninstall -y nltk
/home/ec2-user/anaconda3/envs/python3/bin/python -m pip install -U nltk==3.8.1

EOF
