import logging
from botocore.exceptions import ClientError
import boto3
import botocore
import paramiko
from scp import SCPClient
import multiprocessing as mp
import time
import sys


def create_ec2_instance(image_id, instance_type, keypair_name, GroupName, instance_number):
    """Provision and launch an EC2 instance

    The method returns without waiting for the instance to reach
    a running state.

    :param image_id: ID of AMI to launch, such as 'ami-XXXX'
    :param instance_type: string, such as 't2.micro'
    :param keypair_name: string, name of the key pair
    :return Dictionary containing information about the instance. If error,
    returns None.
    """

    # Provision and launch the EC2 instance
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    try:
        response = ec2_client.run_instances(ImageId=image_id,
                                            InstanceType=instance_type,
                                            KeyName=keypair_name,
                                            SecurityGroups=[GroupName],
                                            MinCount=instance_number,
                                            MaxCount=instance_number)
    except ClientError as e:
        logging.error(e)
        return None
    return list(response['Instances'])


def exercise(number):
    # Exercise create_ec2_instance
    # Assign these values before running the program
    image_id = 'ami-04b9e92b5572fa0d1'
    instance_type = 't2.micro'
    keypair_name = ''  # please add keypair name here
    GroupName = ''  # please add security group here
    instance_number = number

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Provision and launch the EC2 instance
    instance_info = create_ec2_instance(image_id, instance_type, keypair_name, GroupName, instance_number)
    if instance_info is not None:
        logging.info(f'Launched EC2 Instance {instance_info["InstanceId"]}')
        logging.info(f'    VPC ID: {instance_info["VpcId"]}')
        logging.info(f'    Private IP Address: {instance_info["PrivateIpAddress"]}')
        logging.info(f'    Current State: {instance_info["State"]["Name"]}')


# upload job to a single instance newest version
def upload1(data):
    zeros, upper, lower, instances = data
    key = paramiko.RSAKey.from_private_key_file("")  # please add key path here
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ec2 = boto3.resource('ec2')
    # print(instances)
    public_ip = instances
    # print(public_ip)
    try:
        client.connect(hostname=public_ip, username="ubuntu", pkey=key)
        scp = SCPClient(client.get_transport())
        # print("**********************************************")
        scp.put('job.py', recursive=True, remote_path='/home/ubuntu')
        # print("**********************************************")
        stdin, stdout, stderr = client.exec_command(
            'python3 job.py' + ' ' + str(zeros) + ' ' + str(upper) + ' ' + str(lower))

        data = stdout.read().splitlines()
        print(data)
        for line in data:
            if (line.decode()):
                # print(line.decode())
                client.close()
                # ec2.instances.filter(
                #     Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]).terminate()
                return line.decode()
    except Exception as e:
        print(e)
        ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]).terminate()
        sys.exit(0)
        # print("?????????")
        # print('EC2 is boosting, waiting for it to restart!')
    # for instance in instances:


# upload job to multiple instance
def multi_upload(zeros, p_num):
    start = time.perf_counter()
    image_id = 'ami-04b9e92b5572fa0d1'
    instance_type = 't2.micro'
    keypair_name = '' # please add keypair name here
    GroupName = ''  # please add security group here
    instance_number = p_num
    instance_info = create_ec2_instance(image_id, instance_type, keypair_name, GroupName, instance_number)
    ids = []
    for i in range(len(instance_info)):
        ids.append(instance_info[i]["InstanceId"])
    print(ids)
    # if instance_info is not None:
    #     print((f'    Current State: {instance_info["State"]["Name"]}'))
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.filter(InstanceIds=ids):
        while instance.state['Name'] != 'running':
            # print("wokazhule!")
            # print("...instance is %s" % instance.state['Name'])
            # time.sleep(1)
            instance.load()
    time.sleep(20)
    # print("all instance are good!")
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    IPs = []
    for instance in instances:
        IPs.append(instance.public_ip_address)
    # print(IPs)
    zero_list = [zeros] * p_num
    current_list = range(0, p_num)
    p_num_list = [p_num] * p_num
    # range_list = range(int(ranges / p_num), ranges + int(ranges / p_num), int(ranges / p_num))
    r = int(2**32/p_num)
    lower_list = list(range(0, p_num*r, r))
    upper_list = range(r, (p_num+1)*r, r)
    upper_list = list(upper_list)
    upper_list[-1] = 2**32
    # print(lower_list)
    # print(upper_list)
    # end1 = time.perf_counter()
    # print(f'AWS prepare time is {round(end1 - start1, 2)} second(s)')
    # start = time.perf_counter()
    tp = list(zip(zero_list, current_list, p_num_list, IPs))
    # print(tp)
    # print(tp)
    p = mp.Pool(processes=p_num)
    golden_nonce = None
    # result = p.starmap(upload1, tp)
    s = time.perf_counter()
    for result1 in p.imap_unordered(upload1,tp):
        if result1 != None:
            golden_nonce = result1
            instances.terminate()
            break
    f = time.perf_counter()
    print(f'Task t finished in {round(f - s, 6)} second(s)')
    print(golden_nonce)
    # p.close()
    # p.join()
    # if all(x is None for x in result):
    #     print("Can't find such a nonce")
    #     instances.terminate()
    # print(result[0])
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')


# upload job to a single instance
def upload():
    key = paramiko.RSAKey.from_private_key_file("C:/Users/Xingyang Zhou/.ssh/wing_cloud.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    print("----------------------")
    instances_list = list(instances)
    print(instances_list[0].public_ip_address)
    print("----------------------")
    # print(instances[0])
    for instance in instances:
        print(instance)
        print(instance.id, instance.instance_type, instance.public_ip_address)
        public_ip = instance.public_ip_address
        try:
            client.connect(hostname=public_ip, username="ubuntu", pkey=key)
            scp = SCPClient(client.get_transport())
            scp.put('Task_T.py', recursive=True, remote_path='/home/ubuntu')
            stdin, stdout, stderr = client.exec_command('python3 Task_T.py')
            # print(stdout.read())
            data = stdout.read().splitlines()
            for line in data:
                if(line.decode()):
                    print(line.decode())
                    client.close()
                    ec2.instances.filter(
                        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]).stop()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # main()
    multi_upload(32, 8)
    # upload()