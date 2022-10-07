from django.test import TestCase
import json
from graphene_django.utils.testing import GraphQLTestCase

# Create your tests here.

class QueryTestCase(GraphQLTestCase):

    def test_query_1(self):
        response = self.query(
            '''
            {
                allPosts {
                    title
                    publishedDate
                }
            }
            '''
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
    
    def test_mutation_1(self):
        response = self.query(
            '''
            mutation {
                createPost(input:{
                    title:"Test Title", 
                    body:"Test body", 
                    author:1, 
                    publishedDate:"2016-07-20T17:30:15+05:30", 
                    status:false
                })
                {
                    post {
                    title
                    }
                }
            }
            '''
        )

        self.assertResponseNoErrors(response)