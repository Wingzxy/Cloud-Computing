import logging
from botocore.exceptions import ClientError
import boto3
import botocore
import paramiko
from scp import SCPClient
import multiprocessing as mp
import time


def create_ec2_instance(image_id, instance_type, keypair_name, GroupName):
    ec2 = boto3.resource('ec2', 'us-east-1')
    startup = open("boot.sh").read()
    try:
        response = ec2.create_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            SecurityGroups=[GroupName,],
                                            MinCount=1,
                                            MaxCount=1,
                                            UserData=startup)
    except ClientError as e:
        logging.error(e)
        return None
    return response[0]


def create_sqs_queue(queue_name):
    sqs = boto3.resource('sqs', 'us-east-1')
    response = sqs.create_queue(
        QueueName= queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400'
        }
    )
    return response

def upload2(zeros, ranges, p_num):
    image_id = 'ami-04b9e92b5572fa0d1'
    instance_type = 't2.micro'
    keypair_name = '' # please fill in keypair name
    GroupName = '' # please fill in security group name
    instance_number = p_num
    margin = int(2 ** (ranges) / p_num)
    queue_name = 'My_queue'
    sqs = create_sqs_queue(queue_name)
    for current_range in range(instance_number):
        instance_info = create_ec2_instance(image_id, instance_type, keypair_name, GroupName)
        print(instance_info)
        while instance_info.state['Name'] != 'running':
            instance_info.load()
        time.sleep(90)
        print("all instance are good!")
        key = paramiko.RSAKey.from_private_key_file("") # please fill in key.pem path
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ec2 = boto3.resource('ec2')
        ip = instance_info.public_ip_address

        try:
            client.connect(hostname=ip, username="ubuntu", pkey=key)
            scp = SCPClient(client.get_transport())
            scp.put('Task.py', recursive=True, remote_path='/home/ubuntu')
            command = 'python3 Task.py' + ' ' + str(zeros) + ' ' + str(current_range) + ' ' + str(margin) + ' ' + str(sqs.url)
            stdin, stdout, stderr = client.exec_command(
                command)
            client.close()
        except ClientError as e:
            print(e)
    received = retrieve_sqs_messages('https://queue.amazonaws.com/592443159497/My_queue')
    try:
        print(received['Messages'][0]['Body'])
    except:
        print("Didn't receive any message")
    ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]).terminate()
    sqs.delete()


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=0):

    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    sqs_client = boto3.client('sqs')
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
    except ClientError as e:
        logging.error(e)
        return None

    return msgs



if __name__ == '__main__':
    start = time.perf_counter()
    upload2(16,32,8)
    end = time.perf_counter()
    print(f'Finished in {round(end - start, 2)} second(s)')
