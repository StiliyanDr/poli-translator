import datetime as dt
from decimal import Decimal
from typing import NamedTuple

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from dynamodb import error as ddberror


class Comment(NamedTuple):
    """
    Represents a comment
    """
    username: str
    datetime: dt.datetime
    text: str = ""


class Comments:
    """
    Represents a DynamoDB table with comments data:
     - username (HASH)
     - datetime (RANGE)
     - text
    """
    __ATTRIBUTES = [
        {"AttributeName": "username", "AttributeType": "S"},
        {"AttributeName": "datetime", "AttributeType": "N"},
    ]

    __KEY_SCHEMA = [
        {"AttributeName": "username", "KeyType": "HASH"},
        {"AttributeName": "datetime", "KeyType": "RANGE"},
    ]

    __THROUGHPUT = {
        "ReadCapacityUnits": 10,
        "WriteCapacityUnits": 10,
    }

    def __init__(self, dynamo, name="Comments"):
        """
        Loads a table or creates one, if it doesn't exist.

        :param dynamo: a DynamoDB boto3.resource
        :param name: a str - the name of the table, defaults to
        'Comments'.
        """
        self.__dynamo = dynamo
        self.__load_or_create_table(name)

    def __load_or_create_table(self, name):
        self.__table = self.__load_table(name)

        if self.__table is None:
            self.__table = self.__create_table(name)

    def __load_table(self, name):
        try:
            table = self.__dynamo.Table(name)
            table.load()
        except ClientError as e:
            if not ddberror.is_resource_not_found(e):
                raise ddberror.Error.from_client_error(e)
            else:
                return None
        else:
            return table

    @ddberror.wrap_client_error
    def __create_table(self, name):
        table = self.__dynamo.create_table(
            TableName=name,
            KeySchema=self.__class__.__KEY_SCHEMA,
            AttributeDefinitions=self.__class__.__ATTRIBUTES,
            ProvisionedThroughput=self.__class__.__THROUGHPUT
        )
        table.wait_until_exists()

        return table

    @ddberror.wrap_client_error
    def add_comment(self, comment):
        """
        Adds a comment to the table.

        :param comment: an instance of Comment.
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()
        self.__table.put_item(
            Item=self.__class__.__comment_to_json(comment)
        )

    @staticmethod
    def __comment_to_json(c):
        return {
            "username": c.username,
            "datetime": int(c.datetime.timestamp()),
            "text": c.text,
        }

    def __verify_table_exists(self):
        if self.__table is None:
            raise ddberror.Error("Table does not exist!")

    @ddberror.wrap_client_error
    def add_comments(self, comments):
        """
        Adds multiple comments to the table.

        :param comments: an iterable of Comment instances.
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()

        with self.__table.batch_writer() as writer:
            for c in comments:
                writer.put_item(
                    Item=self.__class__.__comment_to_json(c)
                )

    @ddberror.wrap_client_error
    def get_comment(self, username, datetime):
        """
        :param username: a str.
        :param datetime: a datetime instance.
        :returns: a Comment instance (or None).
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()

        item = self.__table.get_item(Key={
            "username": username,
            "datetime": int(datetime.timestamp())
        }).get("Item")

        return (self.__class__.__parse_comment(item)
                if item is not None
                else None)

    @staticmethod
    def __parse_comment(c):
        return Comment(username=c["username"],
                       datetime=dt.datetime.fromtimestamp(
                           int(c["datetime"])
                       ),
                       text=c.get("text", ""))

    @ddberror.wrap_client_error
    def update_comment(self, username, datetime, new_text):
        """
        Updates a comment, if it exists. Otherwise, creates a new one.

        :param username: a str.
        :param datetime: a datetime instance.
        :param new_text: a str.
        :returns: the comment as it looks now.
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()

        response = self.__table.update_item(
            Key={"username": username,
                 "datetime": int(datetime.timestamp())},
            UpdateExpression="set #txt=:t",
            ExpressionAttributeNames={
                "#txt": "text",
            },
            ExpressionAttributeValues={
                ":t": new_text,
            },
            ReturnValues="ALL_NEW"
        )

        return self.__class__.__parse_comment(response["Attributes"])

    @ddberror.wrap_client_error
    def query(self, username):
        """
        Queries for comments made by a specific user.

        :param username: a str.
        :returns: a list of the Comments.
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()

        response = self.__table.query(
            KeyConditionExpression=Key("username").eq(username)
        )

        return [self.__class__.__parse_comment(i)
                for i in response["Items"]]

    @ddberror.wrap_client_error
    def delete_comment(self, username, datetime):
        """
        :param username: a str.
        :param datetime: a datetime instance.
        :raises Error: if the table does not exist.
        """
        self.__verify_table_exists()

        self.__table.delete_item(Key={
            "username": username,
            "datetime": int(datetime.timestamp())
        })

    @ddberror.wrap_client_error
    def delete(self):
        """
        Deletes the table.
        """
        if self.__table is not None:
            self.__table.delete()
            self.__table = None


if __name__ == "__main__":
    import os

    session = boto3.session.Session(
        profile_name=os.getenv("AWS_PROFILE")
    )
    dynamo = session.resource("dynamodb")
    comments = Comments(dynamo)

    d = dt.datetime.fromtimestamp(1692249109)
    comment = comments.get_comment("thomasshelby", d)
    print(comment)
