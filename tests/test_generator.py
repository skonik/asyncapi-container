import json

from asyncapi_container.asyncapi.generators.v3.generator import AsyncAPISpecV3Generator
from asyncapi_container.asyncapi.spec.v3.info import Info
from asyncapi_container.asyncapi.spec.v3.tag import Tag
from asyncapi_container.containers.v3.simple_channels import TopicV3
from asyncapi_container.containers.v3.simple_spec import SimpleSpecV3
from asyncapi_container.custom_types import RoutingMap
from pydantic import BaseModel, Field
from jsonschema import validate

from tests.constants import JsonSchema


class Customer(BaseModel):
    first_name: str = Field(..., title='First Name')
    last_name: str = Field(..., title='Last Name')
    email: str = Field(..., title='Email')
    country: str = Field(..., title='Country')
    zipcode: str = Field(..., title='Zipcode')
    city: str = Field(..., title='City')
    street: str = Field(..., title='Street')
    apartment: str = Field(..., title='Apartment')


class OrderSchemaV1(BaseModel):
    product_id: int = Field(..., title='Product Id')
    quantity: int = Field(..., title='Quantity')
    customer: Customer


class MySpecialServiceAsyncAPISpecV3(SimpleSpecV3):
    info: Info = Info(
        title="My special Service",
        version="1.0.0",
        description="Service for making orders"
    )
    sends: RoutingMap = {
        "shop.orders.v1": [
            OrderSchemaV1,
        ],
        TopicV3(
            address="test.topic.v1",
            title="TESTING TITLE",
            description="test",
            summary="testing summary",
            tags=[
                Tag(name="test"),
            ]
        ): [
            OrderSchemaV1
        ]
    }
    receives: RoutingMap = {
        TopicV3(
            address="test.topic.v1",
            title="TESTING TITLE",
            description="test",
            summary="testing summary",
            tags=[
                Tag(name="test"),
            ]
        ): [
            Customer
        ]
    }


def test_generator_asyncapi_v3_jsons_schema():
    """ Smoke test for asyncapi generator. """

    # GIVEN:
    #   - asyncapi v3 generator
    #   - asyncapi v3 json schema
    asyncapi_generator = AsyncAPISpecV3Generator(
        asyncapi_spec_container=MySpecialServiceAsyncAPISpecV3(),
    )
    asyncapi_v3_definition = asyncapi_generator.as_dict()
    asyncapi_v3_json_schema = json.loads(JsonSchema.ASYNCAPI_V3.read_bytes())
    # WHEN:
    #   - we validate asyncapi v3 generated by generator using asyncapi v3 json schema
    validate(instance=asyncapi_v3_definition, schema=asyncapi_v3_json_schema)
    # THEN:
    #   - no errors raised
