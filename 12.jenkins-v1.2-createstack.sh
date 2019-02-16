aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--stack-name jenkins-v102 \
--template-body file://jenkins-v1.2-settime.template \
--parameters ParameterKey=KeyPair,ParameterValue=EffectiveDevOpsAWS
