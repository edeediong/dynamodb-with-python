from ast import Expression
import boto3

def update_book(book_id, title, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')

    response = books_table.update_item(
        Key={
            'book_id' : 1001,
            'title': "Americanah"
        },
        UpdateExpression="set ISBN=:ISBN",
        ExpressionAttributeValues={':ISBN': "9780307455925"},
        ReturnValues="UPDATED_NEW"
    )
    return response


if __name__ == '__main__':
    update_response = update_book(1001, 'Americanah')
    print(update_response)

