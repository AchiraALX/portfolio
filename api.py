#!/usr/bin/env python3
from graphene import ObjectType, Schema, String


class Query(ObjectType):
    """_summary_

    Args:
        ObjectType (_type_): _description_

    Returns:
        _type_: _description_
    """
    hello = String()

    def resolve_hello(self, info):
        """_summary_

        Args:
            info (_type_): _description_

        Returns:
            _type_: _description_
        """
        return "Hello world."


schema = Schema(query=Query)
result = schema.execute('{ hello }')

print(result.data['hello'])
