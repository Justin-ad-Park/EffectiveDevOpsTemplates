aws cloudformation describe-stacks \
--stack-name jenkins-v102 \
--query 'Stacks[0].Outputs[0]'

