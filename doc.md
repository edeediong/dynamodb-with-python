NoSQL databases are non-tabular databases that store and retrieve data differently from SQL databases. While SQL is table-based, NoSQL databases are either key-value pairs. NoSQL databases are for large distributed systems due to their fast and highly scalable systems.
DynamoDB is an example of a NoSQL database. [DynamoDB](https://aws.amazon.com/dynamodb/) is fast, capable of handling multiple requests, and highly scalable. Dynamo is a NoSQL database provided by Amazon Web Service (AWS). Python is one of the most widely used programming languages and has good support for DynamoDB using the AWS SDK for Python.

In this tutorial, we will be using the Boto3 library to create and query tables, load data, and perform CRUD operations in DynamoDB and Python.

## Prerequisites

- [An AWS account](https://aws.amazon.com/)
- Basic knowledge of [DynamoDB](https://aws.amazon.com/dynamodb/)
- [Python](https://www.python.org/)
- Operating system: Windows, macOS, or Linux.

## Getting started with DynamoDB using Python

DynamoDB as an AWS service allows you to create database tables that store, retrieve data and handle request traffic. AWS offers a set of SDKs for interacting with DynamoDB. These SDKs are available for various programming languages. The AWS SDK for Python is known as [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

We will be using Boto3 to interact with DynamnoDB. AWS Boto3 allows you to create, configure, and manage different AWS services.

### Connecting to the DynamoDB using Python (Boto3)

First, install Boto3 by running the following command on your terminal.

```python
pip install boto3
```

Next, in your code editor, create a `dynamo-python.py` file, and import the Boto3 library at the top of the file.

```python
import boto3
```

Lastly, we will create the Boto3 DynamoDB resource. This will connect to the local instance of our DynamoDB server. Do this by adding this line of code:

```python
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
```

## Creating a table in DynamoDB

We will be creating a table using the Dynamo `create_table` function. Here we call the table *"Books."*

This table will contain attributes for the partition key and the sort key. The “*title*” of the book will be our sort key, and the “*book_id*” will be our partition key.

A **sort key** is a field in a database that indicates the order in which data is stored (in sorted order by the sort key value). In DynamoDB, the sort key for each field is unique.

The **partition key** is the attribute that identifies an item in a database. Data with the same partition key are stored together to enable you to query the data. The data of a partition key is sorted using the sort key.

Now, add the code snippet below to create a table:

```python
import boto3

def create_books_table(dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb')
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
                'AttributeName': 'book_id',
                # AttributeType refers to the data type 'N' for number type and 'S' stands for string type.
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table

if __name__ == '__main__':
    book_table = create_books_table()
    print("Status:", book_table.table_status)
```

In the code above, we created a table named **Books.** The `book_id` would be the partition key, and the title would be the sort key. Next, we defined our table by declaring a key schema stored in the `KeySchema` variable.

We also declared the data types of the attributes. Where "N" represents a number and "S" represents a string, we also added the `ProvisionedThroughput` variable, to reduce the number of "*read*" and "write" operations on the database per second.

Lastly, in the last section of the code snippet, we created an instance of our class.

## Adding sample data to the DynamoDB table

In this section, we will be adding sample data to the DynamoDB table. This data will be written in *JSON* format. To begin, create a JSON file, `data.json`, and add the following data:

```json
[
    {
        "book_id": 1000,
        "title": "Atomic habits",
        "author": "James Clear",
        "isbn": "34526767",
        "year_of_publication": "2019"
    },
    {
        "book_id": 1001,
        "title": "Americanah",
        "author": "Chimamanda Adichie",
        "isbn": "10202223",
        "year_of_publication": "2013"
    },
    {
        "book_id": 1002,
        "title": "Teller of secrets",
        "author": "Bisi Adjapon",
        "isbn": "10201120",
        "year_of_publication": "2013"
    },
    {
        "book_id": 1003,
        "title": "Joys of motherhood",
        "author": "Buchi Emecheta",
        "isbn": "10110120",
        "year_of_publication": "1979" 
    },
    
    {
        "book_id": 1004,
        "title": "Purple Hibiscus",
        "author": "Chimamanda Adichie",
        "isbn": "10001241",
        "year_of_publication": "2012" 
    }
]

```

Now, we need to load this data to add the data to our database. Create a Python file, `store_data.py`, and add these lines of code:

```python
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
```

In the code above, we created a function that will loop through the fields and load the data contained in our *JSON* file. 

Run the following command in your terminal to execute the script above. 

```python
python store_data.py
```

Once the script is running successfully, the result of your loaded data will be displayed on your terminal.

```python
Displaying book data: 1000 Atomic habits
Displaying book data: 1001 Americanah
Displaying book data: 1002 Teller of secrets
Displaying book data: 1003 Joys of motherhood
Displaying book data: 1004 Purple Hibiscus
```

Successful! Good job so far!

## CRUD operations in DynamoDB using Python

We have successfully created a table that contains data (items) and each of these items makes up a set of attributes. These are the core components of DynamoDB.

In this section, we will be working on performing CRUD operations using the items in our DynamnoDB table.

*Let’s dive in!*

### **Create item**

We will use the `put_item()` method to add new items to the *Books* table. To get started, create a new python file, `add_book.py`, and add the following code snippet:

```python
import boto3

def add_book(books, dynamodb=None):
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
    book_resp = add_book(books='Books')
    print(book_resp)
```

In the code snippet above, we defined a function that will add items from our Dynamo table. Next, using the `put_item()` method, we added sample data to add to the DynamoDB table.

Run the scripts in your terminal to add the data:

```python
python add_book.py
```

You should get this output:

```bash
{'ResponseMetadata': {'RequestId': '', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 05 May 2022 15:00:40 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': '', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
```

### **Read item**

We can also access the item(s) in the DynamoDB table using the `get_item()` method. We need the primary to be able to access the database. The primary of this project is a combination of the sort key (’*title*’) and the partition key *(’book_id’)*.

Create a python file, `get_book.py`, and add the following lines of code:

```python
import boto3
from botocore.exceptions import ClientError

def get_book(book_id, title, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')

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
```

From the code above, we imported `ClientError` from the `botocore.exceptions` package, which is set to help us navigate and handle errors and exceptions that you may encounter while interacting with the AWS Boto3 SDK.

Run this script on your terminal using this command:

```python
python get_book.py
```

You should get this output:

```python
{'year_of_publication': '2019', 'isbn': '34526767', 'book_id': Decimal('1000'), 'author': 'James Clear', 'title': 'Atomic habits'}
```

### Condition Expressions

When working with DynamoDB, you are likely to use `ConditionExpressions` when altering items in a database table. 

[Condition Expressions](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#dynamodb-conditions) are optional parameters used to manipulate specified items in a DynamoDB table. Conditions Expressions are applied using the `PutItem`, `UpdateItem`, and `DeleteItem` operations. 

These operations are implemented when updating or deleting items. The operation only succeeds if the condition expression value is set to true; else, the operation fails.

In the next section, we will be working with condition expressions for updating and deleting items on our table.

### **Update item**

We can also update the existing data in our table. This is done by either updating the values of an existing attribute, adding new attributes, or deleting attributes.

In this section, we will update the value of an existing attribute using the `update_item()` method. Let’s get started with an existing attribute in our table:

```python
     {
        "book_id": 1001,
        "title": "Americanah",
        "author": "Chimamanda Adichie",
        "isbn": "10202223",
        "year_of_publication": "2013"
    }
```

Create a python file, `update_book.py`, and these lines of code:

```python
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
```

From the code above, we defined a function that will add items from our Dynamo table. Next, using the `update_item()` method, we intend to update an attribute in the DynamoDB table. Other parameters used include:

**UpdateExpression:** Defines attribute(s) which are to be updated and their new values.

**ExpressionAttributeValues:** This expression holds the substitutes for the attribute to be updated or the new value.

**ReturnValues:** Use this parameter to get the item attributes before or after they are updated. For `UpdateItem()`, the valid values are **NONE | ALL_OLD | UPDATED_OLD | ALL_NEW | UPDATED_NEW**.

Run this script on your terminal using this command:

```python
python update_book.py
```

**Output**:

```python
{'Attributes': {'ISBN': '9780307455925'}, 'ResponseMetadata': {'RequestId': '3TJHT8856E3GRKFCPN8S5HMRQ3VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 09 May 2022 10:26:53 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '45', 'connection': 'keep-alive', 'x-amzn-requestid': '3TJHT8856E3GRKFCPN8S5HMRQ3VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2958762950'}, 'RetryAttempts': 0}}
```

### **Delete item**

For the last CRUD operation, we will be deleting an item from our table using the `delete_item()` method. You can either use the primary key of the item or a `ConditionExpression` to delete the item. If you wish to use a `ConditionExpression` the condition expression value must be set to true.
However, in this tutorial, we will be using both the primary key and the condition expression.

Create a python file, `delete_book.py`, and these lines of code:

```python
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
```

Run this script on your terminal using this command:

```python
python delete_book.py
```

**Output:**

```python
{'ResponseMetadata': {'RequestId': 'LQ2M5SKSNKAASF041VPKE6FQCFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 09 May 2022 11:56:08 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': 'LQ2M5SKSNKAASF041VPKE6FQCFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
```

## Query Tables in DynamoDB

Querying our database table returns every item in the table with the same partition key. We will query the table using the value of our partition key using the `query()` method. The partition key in this project is *‘book_id’.*

*Let’s dive in!*

Create a python file, `query_table.py`, and these lines of code:

```python
import boto3 
from boto3.dynamodb.conditions import Key 

def query_book(book_id, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')

    response = books_table.query(
        KeyConditionExpression=Key('book_id').eq(1001)
    )
    return response['Items']

if __name__ == '__main__':
    query_id = 10001
    print(f"Book ID: {query_id}")
    books_data = query_book(query_id)
    for book_data in books_data:
       print(book_data['book_id'], ":", book_data['title'])
```

Run this script on your terminal using this command:

```python
python query_table.py **Outputt**
```

**Output:**

```python
Book ID: 10001
1001: Americanah
```

## Delete Table

In addition to CRUD operations, you can also delete an entire DynamoDB table using the `table.delete()` method. All that is required is that you specify the name of the table you wish to delete.

Create a python file, `delete_table.py`, and these lines of code:

```python

import boto3

def delete_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb')

    books_table = dynamodb.Table('Books')
    books_table.delete()

if __name__ == '__main__':
    delete_table()
    print("DynamoDB table deleted!")
```

Run this script on your terminal using this command:

```python
python delete_table.py
```

**Output:**

```python
DynamoDB table deleted
```

## Conclusion

Several DynamoDB operations can be performed by creating a Python script using AWS Boto3. In this tutorial, we created a DynamoDB table using Boto3 to interact with our database and perform CRUD operations, query, and delete a table.

I hope you had fun working on this!

Happy Coding!🙂