import json 
from decimal import Decimal
import boto3 



def load_data(books, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb')

    books_table = dynamodb.Table('Books')
    for book in books:
        book_id = (book['book_id'])
        title= book['title']

        print("Displaying book data:", book_id, title)
        books_table.put_item(Item=book)


if __name__ == '__main__':

    with open("data.json") as json_file:
        book_list = json.load(json_file, parse_float=Decimal)
    load_data(book_list)