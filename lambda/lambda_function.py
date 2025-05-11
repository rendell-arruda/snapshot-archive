import boto3

def assume_role(account_id, role_name):
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

def listar_snapshots_para_arquivar(session):
    ec2 = session.client('ec2')
    #busca por snapshots na conta
    response = ec2.describe_snapshots(OwnerIds=["self"])
    snapshots = response.get("Snapshots", [])
    
    print(f"O total de Snapshots encontrados: {len(snapshots)}")
    return snapshots    
 
if __name__ == "__main__":
    # Substitua com os dados reais
    destino_account_id = 471112936182
    role_name = "SnapshotArchiveRole"

    # Assume a role e cria a sessão
    session = assume_role(destino_account_id, role_name)

    # Lista os snapshots
    snapshots = listar_snapshots_para_arquivar(session)
    
    #imprime os snapshots
    for snapshot in snapshots:
        print(f"Snapshot ID: {snapshot['SnapshotId']}, Description: {snapshot.get('Description', 'No description')}")