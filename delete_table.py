import boto3


def delete_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')
    books_table.delete()

d
if __name__ == '__main__':
    delete_table()
    print("DynamoDB table deleted.")