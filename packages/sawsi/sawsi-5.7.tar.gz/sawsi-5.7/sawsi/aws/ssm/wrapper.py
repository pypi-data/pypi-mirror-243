import boto3
from typing import List


class SSM:
    def __init__(self, boto3_session, region_name='us-east-1'):
        self.client = boto3_session.client('ssm', region_name=region_name)
        self.region = boto3_session.region_name

    def run_commands(self, instance_id:str, commands: List[str]):
        response = self.client.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': commands}
        )
        command_id = response['Command']['CommandId']
        output = self.client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )
        return output


