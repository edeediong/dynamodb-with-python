import boto3

def create_books_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb')
 
    table = dynamodb.create_table(
        TableName='Books',
        KeySchema=[
            {
                'AttributeName': 'book_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'book_id', # AttributeType refers to the data type 'N' represents number. 
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S' # 'S' represents String data type
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10, 
            'WriteCapacityUnits': 10  
        }
    )
    return table


if __name__ == '__main__':
    book_table = create_books_table()
    print("Status:", book_table.table_status)




