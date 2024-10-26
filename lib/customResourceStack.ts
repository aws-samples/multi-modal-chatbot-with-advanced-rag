import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as cr from 'aws-cdk-lib/custom-resources';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

interface CustomResourceStackProps extends cdk.StackProps {
  env: {
    account: string | undefined;
    region: string;
  };
}

export class CustomResourceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: CustomResourceStackProps) {
    super(scope, id, props);

    const domainArn = cdk.Fn.importValue('DomainArn');
    //const DEFAULT_REGION = this.node.tryGetContext('DEFAULT_REGION');
    const DEFAULT_REGION = props.env.region;
    
    const lambdaRole = new iam.Role(this, 'LambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });

    lambdaRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
    );

    lambdaRole.addToPolicy(new iam.PolicyStatement({
      actions: ['es:AssociatePackage', 'es:DescribePackages', 'es:DescribeDomain', 'logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents'],
      resources: ["*"], //"*"
    }));

    
    const customResourceLambda = new lambda.Function(this, 'CustomResourceLambda', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.on_event',
      code: lambda.Code.fromAsset('lambda'),
      timeout: cdk.Duration.minutes(15),
      role: lambdaRole
    });

    //const isCompleteLambda = new lambda.Function(this, 'IsCompleteLambda', {
    //  runtime: lambda.Runtime.PYTHON_3_9,
    //  handler: 'index.is_complete',
    //  code: lambda.Code.fromAsset('lambda'),
    //  timeout: cdk.Duration.minutes(15),
    //  role: lambdaRole
    //});

    
    const customResourceProvider = new cr.Provider(this, 'CustomResourceProvider', {
      onEventHandler: customResourceLambda,
      //isCompleteHandler: isCompleteLambda,
      //queryInterval: cdk.Duration.minutes(1),
      //totalTimeout: cdk.Duration.hours(1),
    });
    
    
    const customResource = new cdk.CustomResource(this, 'AssociateNoriPackage', {
      serviceToken: customResourceProvider.serviceToken,
      properties: {
        DomainArn: domainArn,
        DEFAULT_REGION: DEFAULT_REGION,
        VERSION: "2.11",
      },
    });
  }
}