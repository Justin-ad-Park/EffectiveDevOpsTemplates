aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--stack-name dev-batch \
--template-body file://jenkins-v1.2-settime.template \
--parameters ParameterKey=KeyPair,ParameterValue=pmo_aws
