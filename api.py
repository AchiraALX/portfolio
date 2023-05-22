#!/usr/bin/env python3
from graphene import ObjectType, Schema, String

class Query(ObjectType):
    hello = String()
    def resolve_hello(self, info):
        return "Hello world."

schema = Schema(query=Query)
result = schema.execute('{ hello }')

print(result.data['hello'])