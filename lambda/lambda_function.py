import boto3
from botocore.exceptions import ClientError

# Função para assumir uma role em outra conta AWS
def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='SnapshotArchiveSession'
    )

    credentials = response['Credentials']

    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'
    )

    return session

# Lista todos os snapshots da conta (proprietário = self)
def listar_snapshots_para_arquivar(session):
    ec2 = session.client('ec2')
    response = ec2.describe_snapshots(OwnerIds=["self"])
    snapshots = response.get("Snapshots", [])
    print(f"O total de Snapshots encontrados: {len(snapshots)}")
    return snapshots    

# Filtra snapshots que estão no tier padrão
def filter_snapshots_standart(session, snapshots):
    snapshots_standart = []
    for snap in snapshots:
        storage_tier = snap.get("StorageTier", "standard")
        snapshot_id = snap.get("SnapshotId", "sem ID")
        print(f"DEBUG: Snapshot {snapshot_id} está no tier {storage_tier}")
        if storage_tier == "standard":
            snapshots_standart.append(snap)
    return snapshots_standart

# Arquiva snapshots, com suporte a dry run
def arquivar_snapshots(session, snapshots, dry_run=True):
    ec2 = session.client('ec2')
    
    for snap in snapshots:
        snapshot_id = snap['SnapshotId']
        storage_tier = snap.get('StorageTier', 'standard')

        if storage_tier == 'archive':
            print(f"Snapshot {snapshot_id} já está no tier archive. Ignorando.")
            continue

        try:
            response = ec2.modify_snapshot_tier(
                SnapshotId=snapshot_id,
                StorageTier='archive',
                DryRun=dry_run
            )
            print(f"[DRY-RUN={dry_run}] Snapshot {snapshot_id} arquivado com sucesso.")

        except ClientError as e:
            if e.response['Error']['Code'] == 'DryRunOperation':
                print(f"[DRY-RUN={dry_run}] A chamada funcionaria: Snapshot {snapshot_id} pode ser arquivado.")
            else:
                print(f"Erro ao arquivar snapshot {snapshot_id}: {e}")

# Execução principal
if __name__ == "__main__":
    destino_account_id = 471112936182
    role_name = "SnapshotArchiveRole"

    session = assume_role(destino_account_id, role_name)

    todos_snapshots = listar_snapshots_para_arquivar(session)
    standart_snapshots = filter_snapshots_standart(session, todos_snapshots)

    for snap in standart_snapshots:
        print(f"Snapshot ID: {snap['SnapshotId']}, Description: {snap.get('Description', 'No description')} está no tier {snap.get('StorageTier', 'desconhecido')}")

    # Aqui você define se quer simular (dry_run=True) ou realmente arquivar (dry_run=False)
    arquivar_snapshots(session, standart_snapshots, dry_run=True)