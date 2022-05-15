import boto3

def delete_book(book_id, title, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')

    response = books_table.delete_item(
        Key={
            'book_id' : 1001,
            'title': "Americanah"
        },
        ConditionExpression="ISBN=:ISBN",
        ExpressionAttributeValues={':ISBN': "9780307455925"},
        
    )
    return response


if __name__ == '__main__':
    delete_response = delete_book(1001, 'Americanah')
    print(delete_response)