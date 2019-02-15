aws cloudformation describe-stacks \
--stack-name jenkins \
--query 'Stacks[0].Outputs[0]'

