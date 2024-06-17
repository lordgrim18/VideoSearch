import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

def create_video_table():
    table = dynamodb.create_table(
        TableName='Videos',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'  # String
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    print('Table name:', table.name)
    print('Table created:', table.table_status)
    print('Item count:', table.item_count)
    return table

def create_subtitle_table():
    table = dynamodb.create_table(
        TableName='Subtitles',
        KeySchema=[
            {
                'AttributeName': 'video_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'start_time',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'video_id',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'start_time',
                'AttributeType': 'N'  # Number
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()

    print('Table name:', table.name)
    print('Table created:', table.table_status)
    print('Item count:', table.item_count)
    return table

# Run the functions to create tables
if __name__ == '__main__':
    create_video_table()
    create_subtitle_table()
