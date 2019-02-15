aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--stack-name jenkins \
--template-body file://jenkins-cf.template \
--parameters ParameterKey=KeyPair,ParameterValue=EffectiveDevOpsAWS
