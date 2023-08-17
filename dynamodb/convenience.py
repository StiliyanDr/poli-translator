from dynamodb import error as ddberror


@ddberror.wrap_client_error
def list_tables(dynamo):
    """
    Lists the Amazon DynamoDB tables for the current account.

    :returns: a list of strs - the table names.
    """
    return [
        table.name
        for table in dynamo.tables.all()
    ]
