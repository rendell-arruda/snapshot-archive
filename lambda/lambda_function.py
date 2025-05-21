import boto3

# Função para assumir uma role em outra conta AWS
def assume_role(account_id, role_name):
    sts_client = boto3.client('sts')

    # Monta o ARN da role a ser assumida
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'
    
    # Solicita credenciais temporárias para assumir a role
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='SnapshotArchiveSession'
    )

    credentials = response['Credentials']

    # Cria uma sessão AWS com as credenciais temporárias
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'  # região pode ser ajustada
    )

    return session

# Lista todos os snapshots da conta (proprietário = self)
def listar_snapshots_para_arquivar(session):
    ec2 = session.client('ec2')
    
    response = ec2.describe_snapshots(OwnerIds=["self"])  # Busca todos os snapshots da conta
    snapshots = response.get("Snapshots", [])
    
    print(f"O total de Snapshots encontrados: {len(snapshots)}")
    return snapshots    

# Filtra apenas snapshots que estão no tier padrão (standard)
# def filter_snapshots_standart(session, snapshots):
#     snapshots_standart = []

#     for snap in snapshots:
#         storage_tier = snap.get("StorageTier", "standard")

#         if storage_tier == "standard":
#             snapshots_standart.append(snap)  # Salva o snapshot inteiro

#     return snapshots_standart
def filter_snapshots_standart(session, snapshots):
    snapshots_standart = []

    for snap in snapshots:
        storage_tier = snap.get("StorageTier", "standard")
        snapshot_id = snap.get("SnapshotId", "sem ID")

        print(f"DEBUG: Snapshot {snapshot_id} está no tier {storage_tier}")

        if storage_tier == "standard":
            snapshots_standart.append(snap)

    return snapshots_standart

# Simula o arquivamento de snapshots (etapa real será adicionada depois)
def arquivar_snapshots(session, snapshots):
    ec2 = session.client('ec2')
    
    for snap in snapshots:
        snapshot_id = snap['SnapshotId']
        storage_tier = snap.get('StorageTier', 'standard')

        if storage_tier == 'archive':
            print(f"Snapshot {snapshot_id} já está no tier archive. Ignorando.")
            continue

        # Aqui será feita a chamada real com dry-run no futuro
        print(f"Snapshot {snapshot_id} seria arquivado agora.")

# Execução principal
if __name__ == "__main__":
    # Substitua com a conta de destino e o nome da role
    destino_account_id = 471112936182
    role_name = "SnapshotArchiveRole"

    # Assume a role e cria a sessão com credenciais temporárias
    session = assume_role(destino_account_id, role_name)

    # Lista todos os snapshots
    todos_snapshots = listar_snapshots_para_arquivar(session)
    
    # Filtra os snapshots que estão no tier padrão
    standart_snapshots = filter_snapshots_standart(session, todos_snapshots)
    
    # Exibe os snapshots filtrados
    for snap in standart_snapshots:
        print(f"Snapshot ID: {snap['SnapshotId']}, Description: {snap.get('Description', 'No description')} está no tier {snap.get('StorageTier', 'desconhecido')}")

    # Simula a arquivação dos snapshots padrão
    arquivar_snapshots(session, standart_snapshots)