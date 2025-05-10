def lambda_handler(event, context):
    print("Inicializing Lambda function...")
    return {
        'statusCode': 200,
        'body': 'Lambda executed success!'
    }
 
if __name__ == "__main__":
    lambda_handler({},None)