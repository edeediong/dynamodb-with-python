
c

    try:
        response = books_table.get_item(
            Key={'book_id': book_id, 'title': title})
    except ClientError as e:
            print(e.response['No item found'])
    else:
            return response['Item']


if __name__ == '__main__':
    book = get_book(1000, "Atomic habits")
    if book:
        print(book)
