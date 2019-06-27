aws cloudformation create-stack \
--capabilities CAPABILITY_IAM \
--stack-name real-jenkins-batch \
--template-body file://ec2_jenkins_server.template \
--parameters \
ParameterKey=KeyName,ParameterValue=pmo_aws \
ParameterKey=InstanceName,ParameterValue=real_jenkins \
ParameterKey=VpcId,ParameterValue=vpc-011c655372cdf5ad0 \
ParameterKey=SubnetId,ParameterValue=subnet-0d6a0eefdcc085f7c \
ParameterKey=PrimaryIPAddress,ParameterValue=128.0.1.1 \
ParameterKey=SSHLocation,ParameterValue=210.180.115.20/32