import boto3

def assume_role(account_id, role_name):
    print("Assuming role...")
    print(f"Account ID: {account_id}, Role Name: {role_name}")
    # Cria um cliente STS
    # Esta função é um espaço reservado para a lógica real de suposição de função.
    sts_client = boto3.client('sts')

    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='SnapshotArchiveSession'
    )

    credentials = response['Credentials']

    # Cria uma sessão com as credenciais temporárias
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    return session

def lambda_handler(event, context):
    print("Inicializing Lambda function...")
    return {
        'statusCode': 200,
        'body': 'Lambda executed success!'
    }
 
if __name__ == "__main__":
    # Substitua com os dados reais
    destino_account_id = "...."
    role_name = "SnapshotArchiveRole"

    session = assume_role(destino_account_id, role_name)

    # Testa chamando EC2 na outra conta
    ec2 = session.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=["self"])  # vai falhar se não houver snapshots ou permissão
    snapshot_name = snapshots.get("Snapshots", [])[0].get("Description", "No description")
    print("Snapshot ID:", snapshot_name)
    # print("Snapshots encontrados:", len(snapshots.get("Snapshots", [])))