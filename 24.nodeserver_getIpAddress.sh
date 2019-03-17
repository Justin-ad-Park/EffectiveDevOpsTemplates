aws cloudformation describe-stacks \
--stack-name helloworld-staging \
--query 'Stacks[0].Outputs[0]'

