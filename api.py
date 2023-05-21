#!/usr/bin/env python3
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="World"))

    def resolve_hell(self, info, name):
        return 'Hello' + name


schema = graphene.Schema(query=Query)
result = schema.execute('{hello}')
print(result.data['hello'])
