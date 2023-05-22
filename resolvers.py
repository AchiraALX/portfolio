#!/usr/bin/env python3
"""Definition of GraphQL API using graphene
"""

from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import (
    ObjectType,
    Field,
    Int,
    Schema
)
from models.user import User as UserModel
from graphql import graphql

class GraphUser(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Query(ObjectType):
    user = Field(GraphUser, id=Int(required=True))

    def resolve_user(self, info, id):
        user = UserModel.query.filter_by(id=id).first()

        if not user:
            raise Exception("User not found.")

        return user

schema = Schema(query=Query)

query = """
    query {
        user(id: 1) {
            id
            username
            email
            name
            }
        }
    """

result = graphql(schema, query)

print(result.data['user'])
