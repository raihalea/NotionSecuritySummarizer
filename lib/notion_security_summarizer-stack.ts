// import * as cdk from 'aws-cdk-lib';
import { Stack, StackProps } from "aws-cdk-lib";
import {
  DockerImageFunction,
  DockerImageCode,
  Architecture,
} from "aws-cdk-lib/aws-lambda";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import { Construct } from "constructs";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class NotionSecuritySummarizerStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const secrets = StringParameter.fromSecureStringParameterAttributes(
      this,
      "NotionApiToken",
      {
        parameterName: "NotionApiToken",
      }
    );

    const registerUrlLambda = new DockerImageFunction(
      this,
      "RegisterUrlLambda",
      {
        code: DockerImageCode.fromImageAsset("./src/lambda/register_url"),
        architecture: Architecture.ARM_64,
        environment: {
          NOTION_SECRETS: secrets.parameterArn,
        },
      }
    );
    secrets.grantRead(registerUrlLambda);

    const getLambda = new DockerImageFunction(this, "GetLambda", {
      code: DockerImageCode.fromImageAsset("./src/lambda/get_docs"),
      architecture: Architecture.ARM_64,
      environment: {
        NOTION_SECRETS: secrets.parameterArn,
      },
    });
    secrets.grantRead(getLambda);
  }
}
