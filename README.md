# Cloud-Computing
Coursework of University of Bristol COMSM0010 <br>
Please fill in the security group name, key pair name in multi_upload function of init.py <br>
Please fill in the path of key.pem file in upload1 fuction of init.py <br>
For mark range from 0-69 please run init.py, you cloud change the parameters of multi_upload function, first is difficulty number D, second is instance numbers <br>
<br>
Run init_B.py to run Method2(Single processing with AWS SQS and SSH) <br>
Change parameters in upload2, first one is difficuty level, last on is instance number, don't modify the middle one, it's an optional search range.<br>
Please fill in the security group name, key pair name in upload2 function of init_B.py <br>
Please fill in the path of key.pem file in upload2 fuction of init_B.py <br>
Please fill in account credentials details in sqs = boto.client() function of Task.py <br>
boot.sh is the bash file for EC2 instances to install pip and boto3 SDK <br>
<br>
Run python3 extension.py T L to try my extension attempt, it is not fully correct, but kindly works<br>
<br>
# Error handle: if it returns any error, need to terminate all instances and do it again. 
