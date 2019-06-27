""" Generating CloudFormation template. """

##### Import library #####
from ipaddress import ip_network

from ipify import get_ip

"""
troposphere : phython script library for template

If do not install library before, run as below script
pip install ipaddress
pip install ipify
pip install troposphere
"""

from troposphere import (
    Base64,
    ec2,
    GetAtt,
    Join,
    Output,
    Parameter,
    Ref,
    Template,
)

from troposphere.iam import (
    InstanceProfile,
    PolicyType as IAMPolicy,
    Role,
)

# Python library for AWS Access Policy Language creation
from awacs.aws import (
    Action,
    Allow,
    Policy,
    Principal,
    Statement,
)

from awacs.sts import AssumeRole

##### Declare variables #####
ApplicationName = "jenkins"
ApplicationPort = "8080"

# for Ansible
GithubAccount = "Justin-ad-Park"
GithubAnsibleURL = "https://github.com/{}/ansible".format(GithubAccount)

AnsiblePullCmd = \
    "/usr/local/bin/ansible-pull -U {} {}.yml -i localhost".format(
        GithubAnsibleURL,
        ApplicationName
    )

# Local PC public ip - For open 22 port
PublicCidrIp = str(ip_network(get_ip()))

######### Template definition ##############
t = Template()

# Template description
t.add_description("Effective DevOps in AWS: HelloWorld web application")


# Delare template parameter
t.add_parameter(Parameter(
    "KeyPair",                                              #parameter name
    Description="Name of an existing EC2 KeyPair to SSH",   #parameter description
    Type="AWS::EC2::KeyPair::KeyName",                      #parameter type
    ConstraintDescription="must be the name of an existing EC2 KeyPair.",   #Constraint description
))

"""
    Security group definition
    22 for SSH, control PC
    8080 for Jenkins, public open
"""
t.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="Allow SSH and TCP/{} access".format(ApplicationPort),
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp=PublicCidrIp,
        ),
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort=ApplicationPort,
            ToPort=ApplicationPort,
            CidrIp="0.0.0.0/0",
        ),
    ],
))

# User defined script. Execute after creating a cloudformation stack
ud = Base64(Join('\n', [
    "#!/bin/bash",
    "yum erase 'ntp*' -y",
    "yum install chrony -y",
    "service chronyd start",    #Service for NTP(network time protocol)
    "chkconfig chronyd on",
    "wget https://bit.ly/2S42vQR -O /etc/sysconfig/clock",  #Configure Asia/Seoul UTC time
    "ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime",
    "yum remove java-1.7.0-openjdk -y",
    "yum install java-1.8.0-openjdk -y",
    "yum install --enablerepo=epel -y git",             #install git from epel repository - /etc/yum.repos.d/epel.repo in EC2
    "pip install ansible",
    AnsiblePullCmd,
    "echo '*/10 * * * * {}' > /etc/cron.d/ansible-pull".format(AnsiblePullCmd)
]))

t.add_resource(Role(
    "Role",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("Service", ["ec2.amazonaws.com"])
            )
        ]
    )
))

t.add_resource(InstanceProfile(
    "InstanceProfile",
    Path="/",
    Roles=[Ref("Role")]
))


t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-0be3e6f84d3b968cd",
    InstanceType="t2.micro",
                        #SubnetId="subnet-96c38dda",   #error
    SecurityGroups=[Ref("SecurityGroup")],
    KeyName=Ref("KeyPair"),
    UserData=ud,
    IamInstanceProfile=Ref("InstanceProfile"),
))

t.add_output(Output(
    "InstancePublicIp",
    Description="Public IP of our instance.",
    Value=GetAtt("instance", "PublicIp"),
))

t.add_output(Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", [
        "http://", GetAtt("instance", "PublicDnsName"),
        ":", ApplicationPort
    ]),
))

print t.to_json()
