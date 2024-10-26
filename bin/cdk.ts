#!/usr/bin/env node
import "source-map-support/register";
import { App } from "aws-cdk-lib";
import { EC2Stack } from "../lib/ec2Stack/ec2Stack";
import { OpensearchStack } from "../lib/openSearchStack";
import { CustomResourceStack } from "../lib/customResourceStack";
import { SagemakerNotebookStack } from "../lib/sagemakerNotebookStack/sagemakerNotebookStack";
import { CfnInclude } from 'aws-cdk-lib/cloudformation-include';

const STACK_PREFIX = "AdvancedRAG";
const DEFAULT_REGION = "us-west-2";
const envSetting = {
  env: {
    account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
    region: DEFAULT_REGION,
  },
};

const app = new App();

// Deploy Sagemaker stack
const sagemakerNotebookStack = new SagemakerNotebookStack(app, `${STACK_PREFIX}-SagemakerNotebookStack`, envSetting);

// Deploy OpenSearch stack
const opensearchStack = new OpensearchStack(app, `${STACK_PREFIX}-OpensearchStack`, envSetting);
opensearchStack.addDependency(sagemakerNotebookStack);

// Deploy Reranker stack using cloudformation template 
const rerankerStack = new CfnInclude(opensearchStack, `${STACK_PREFIX}-RerankerStack`, {
  templateFile: 'lib/rerankerStack/RerankerStack.template.json'
});

const customResourceStack = new CustomResourceStack(app, `${STACK_PREFIX}-CustomResourceStack`, envSetting)
customResourceStack.addDependency(opensearchStack);

// Deploy EC2 stack
const ec2Stack = new EC2Stack(app, `${STACK_PREFIX}-EC2Stack`, envSetting);
ec2Stack.node.addDependency(customResourceStack);

app.synth();
