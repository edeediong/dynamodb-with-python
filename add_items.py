import boto3


def add_item(books, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')
    response = books_table.put_item(
        Item={
        "book_id": 1005,
        "title": "There Was a Country",
        "author": "Chinua Achebe",
        "isbn": "0143124030",
        "year_of_publication": "2012"
    
        }
    )

    
    return response

if __name__ == '__main__':
    book_resp = add_item(books='Books')
    print(book_resp)