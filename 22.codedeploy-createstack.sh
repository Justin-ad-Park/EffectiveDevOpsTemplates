aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--stack-name helloworld-staging \
--template-body file://nodeserver-cf.template \
--parameters ParameterKey=KeyPair,ParameterValue=EffectiveDevOpsAWS
