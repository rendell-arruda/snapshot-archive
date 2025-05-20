import boto3

def assume_role(account_id, role_name):
    # Cria um cliente para o serviço STS (Security Token Service), que permite assumir roles
    sts_client = boto3.client('sts')

    # Monta o ARN da role que será assumida
    role_arn = f'arn:aws:iam::{account_id}:role/{role_name}'

    # Solicita a assunção da role com uma sessão temporária
    response = sts_client.assume_role(
        RoleArn=role_arn,                     # ARN da role alvo
        RoleSessionName='SnapshotArchiveSession'  # Nome arbitrário para a sessão
    )

    # Extrai as credenciais temporárias retornadas pela role assumida
    credentials = response['Credentials']

    # Cria uma sessão boto3 autenticada com as credenciais temporárias
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='us-east-1'  # Região onde os recursos EC2 estão
    )

    return session  # Retorna a sessão para ser usada em outras funções

def listar_snapshots_para_arquivar(session):
    # Cria um cliente EC2 usando a sessão autenticada
    ec2 = session.client('ec2')

    # Lista todos os snapshots criados pela própria conta
    response = ec2.describe_snapshots(OwnerIds=["self"])

    # Pega a lista de snapshots da resposta ou uma lista vazia se não houver
    snapshots = response.get("Snapshots", [])
    
    # Exibe o total de snapshots encontrados
    print(f"O total de Snapshots encontrados: {len(snapshots)}")

    return snapshots  # Retorna os snapshots encontrados   return snapshots    

def filter_snapshots_standart(session, snapshots):
    # Lista para armazenar apenas snapshots no tier padrão
    snapshots_standart = []

    # Itera sobre todos os snapshots recebidos
    for snap in snapshots:
        # Tenta obter o tier do snapshot; assume "standard" se não informado
        storage_tier = snap.get("StorageTier", "standard") # Obtém o tier de armazenamento, padrão é 'standard' se não vier no dicionário

        # Se o snapshot estiver no tier padrão, adiciona à lista
        if storage_tier == "standard":
            snapshots_standart.append(snap)

    return snapshots_standart  # Retorna apenas os snapshots padrão

def arquivar_snapshots(session, snapshots):
    # Cria o cliente EC2 com a sessão autenticada (com assume role, se aplicável)
    ec2 = session.client('ec2')

    for snap in snapshots:
        snapshot_id = snap['SnapshotId']
        try:
            # Chama a API para mover o snapshot para o tier de arquivamento
            response = ec2.modify_snapshot_tier(
                SnapshotId=snapshot_id,
                StorageTier='archive'  # Define o novo tier como "archive"
            )
            print(f"Snapshot {snapshot_id} enviado para o tier 'archive' com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar arquivar snapshot {snapshot_id}: {str(e)}")
 
# Este bloco só será executado se o script for rodado diretamente (não importado como módulo)
if __name__ == "__main__":
    destino_account_id = 471112936182
    role_name = "SnapshotArchiveRole"

    session = assume_role(destino_account_id, role_name)
    todos_snapshots = listar_snapshots_para_arquivar(session)
    standart_snapshots = filter_snapshots_standart(session, todos_snapshots)

    for snap in standart_snapshots:
        print(
            f"Snapshot ID: {snap['SnapshotId']}, "
            f"Description: {snap.get('Description', 'No description')} "
            f"está no tier {snap.get('StorageTier', 'desconhecido')}"
        )

    # Arquiva os snapshots padrão
    arquivar_snapshots(session, standart_snapshots)