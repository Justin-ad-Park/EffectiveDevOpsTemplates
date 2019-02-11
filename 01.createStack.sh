aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ansible --template-body file://helloworld-cf-v2.template --parameters ParameterKey=KeyPair,ParameterValue=EffectiveDevOpsAWS
