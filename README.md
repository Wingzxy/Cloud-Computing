```diff
! Cloud-Computing
Coursework of University of Bristol COMSM0010
Please fill in the security group name, key pair name in multi_upload function of init.py
Please fill in the path of key.pem file in upload1 fuction of init.py
For mark range from 0-69 please run init.py, it is method 1 of my report, you cloud change the parameters of multi_upload function, first is difficulty number D, second is instance numbers

Run init_B.py to run Method2(Single processing with AWS SQS and SSH) 
Run init_C.py to run Method2 but create bunch instance in same time aka Version 2.
Change parameters in upload2, first one is difficuty level, last on is instance number, don't modify the middle one, it's an optional search range.
Please fill in the security group name, key pair name in upload2 function of init_B.py/init_C.py 
Please fill in the path of key.pem file in upload2 fuction of init_B.py/init_C.py 
Please fill in account credentials details in sqs = boto.client() function of Task.py, ie aws_access_key_id, aws_secret_access_key and aws_session_token(if avaliable) 
boot.sh is the bash file for EC2 instances to install pip and boto3 SDK(User Data) 
- If init_B or init_C returns 'Didn't receive any message', please increase the sleep time, it's because boto3 and pip didn't finish installing, it used to takes aournd 90s, but sometime is much more!

Run sudo python3 extension.py T L to try my extension attempt, it is not fully correct, but kindly works

! Error handle: if it returns any error, need to terminate all instances and do it again. 
