import hashlib
import time
from binascii import hexlify
import sys
import boto3


start = time.perf_counter()

orig_message = 'COMSM0010cloud'

def My_CND(zeros, ranges, margin):
    target = (2**(256-zeros))-1

    for nonce in range(ranges*margin, (ranges+1)*margin):
        input_str = str(orig_message) + str(nonce)
        hashval = hashlib.sha256(hashlib.sha256(input_str.encode('utf-8')).digest()).hexdigest()
        if int(hashval, 16) <= target:
            print(nonce)
            return nonce

def Send_result(queue_url, result):
    sqs = boto3.client('sqs', 'us-east-1',
                       aws_access_key_id='',
                       aws_secret_access_key='',
                       aws_session_token='') # please fill in account details, please change region if necessary
    message = ''
    if(result!=None):
        message = 'Found it! The golden nonce is '+ str(result)
    else:
        message = 'Can not find a golden nonce!'
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=message
    )
    print(response['MessageId'])

if __name__ == '__main__':
    a = sys.argv[1]
    b = sys.argv[2]
    c = sys.argv[3]
    # d = sys.argv[4]
    a = int(a)
    b = int(b)
    c = int(c)
    d = 'https://sqs.us-east-1.amazonaws.com/592443159497/My_queue'
    nonce = My_CND(a, b, c)
    Send_result(d, nonce)
# print(nonce)
# finish = time.perf_counter()



# print(f'Finished in {round(finish-start, 2)} second(s)')