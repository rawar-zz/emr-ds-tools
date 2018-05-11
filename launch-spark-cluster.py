import boto3

__author__ = 'rawar'

# please configure your cluster here
AWS_ACCESS_KEY_ID = '<YOUR AWS ACCESS KEY ID>'
AWS_SECRET_ACCESS_KEY = '<YOUR AWS SECRET ACCESS KEY>'
AWS_REGION_NAME = '<YOUR PREFERED REGION>'
S3_LOG_URI = '<S3 URI FOR THE BOOSTRAP LOGGING>'
NOTEBOOKS_URI = '<S3 URI FOR YOUR JUPYTER NOTEBOOKS>'
BOOTSTRAP_SCRIPT = '<S3 URI FOR THE BOOTSTRAP SCRIPT>'
BOOTSTRAP_NAME = 'jupyter-installer'
MASTER_INSTANCE_TYPE = 'm1.large'
WORKER_INSTANCE_TYPE='m1.large'
NUMBER_WORKER_INSTANCES=2
CLUSTER_NAME = 'spark-test-cluster'
AWS_EC2_KEYPAIR_NAME='<SSH KEY-PAIR NAME FOR LOGIN>'
JUPYTER_PWD = '<JUPYTER PASSWORD>'

print('Connect to AWS...')
aws_client = boto3.client(
    'emr',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

print('Try to create a new cluster...')
emr_cluster_id = aws_client.run_job_flow(
    Name=CLUSTER_NAME,
    LogUri=S3_LOG_URI,
    ReleaseLabel='emr-5.13.0',
    Instances={
        'InstanceGroups': [
            {
                'Name': "Master nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': MASTER_INSTANCE_TYPE,
                'InstanceCount': 1,
            },
            {
                'Name': "Worker nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': WORKER_INSTANCE_TYPE,
                'InstanceCount': NUMBER_WORKER_INSTANCES,
            }
        ],
        'Ec2KeyName': AWS_EC2_KEYPAIR_NAME,
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
    },
    Applications=[
    	{
    	    'Name': 'Spark',
    	},
    ],
    Steps=[],
    BootstrapActions=[
        {
            'Name': BOOTSTRAP_NAME,
            'ScriptBootstrapAction': {
                'Path': BOOTSTRAP_SCRIPT,
                'Args': [
                	'JUPYTER_PASSWORD',
                        JUPYTER_PWD,
                	'NOTEBOOK_DIR',
                        NOTEBOOKS_URI,
                ]
            }
        },
    ],
    VisibleToAllUsers=True,
		JobFlowRole='EMR_EC2_DefaultRole',
		ServiceRole='EMR_DefaultRole',
)

print (emr_cluster_id['JobFlowId'])	
print ('Cluster needs some minutes to start and configure...')

