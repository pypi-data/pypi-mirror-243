import json
import tempfile

import pandas as pd
import responses

from fiddler3.entities.model import Model
from fiddler3.schemas.model_schema import ModelSchema
from fiddler3.tests.constants import URL
from fiddler3.tests.utils import assert_approx

DF = df = pd.DataFrame(
    [
        {'col1': 1, 'col2': 'foo'},
        {'col1': 2, 'col2': 'bar'},
        {'col1': 3, 'col2': 'baz'},
    ]
)

API_RESPONSE_200 = {
    'data': {
        'schema_version': 1,
        'columns': [
            {
                'id': 'col1',
                'name': 'col1',
                'data_type': 'int',
                'min': 1,
                'max': 3,
                'bins': [
                    1.0,
                    1.2,
                    1.4,
                    1.6,
                    1.8,
                    2.0,
                    2.2,
                    2.4000000000000004,
                    2.6,
                    2.8,
                    3.0,
                ],
            },
            {
                'id': 'col2',
                'name': 'col2',
                'data_type': 'category',
                'categories': ['bar', 'baz', 'foo'],
            },
        ],
    }
}

API_REQUEST_BODY = {
    'rows': [
        {'col1': '3', 'col2': 'baz'},
        {'col1': '1', 'col2': 'foo'},
        {'col1': '2', 'col2': 'bar'},
    ]
}


@responses.activate
def test_generate_schema_with_dataframe() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )
    schema = Model.generate_schema(source=DF)
    assert isinstance(schema, ModelSchema)
    assert len(schema.columns) == 2

    assert_approx(
        json.loads(responses.calls[0].request.body),
        API_REQUEST_BODY,
        ignore_order=True,
    )


@responses.activate
def test_generate_schema_with_max_cardinality() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )

    max_cardinality = 10
    schema = Model.generate_schema(source=DF, max_cardinality=max_cardinality)
    assert isinstance(schema, ModelSchema)

    request = responses.calls[0].request
    assert json.loads(request.body)['max_cardinality'] == max_cardinality


@responses.activate
def test_generate_schema_with_csv_file() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )

    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as temp_file:
        DF.to_csv(temp_file.name, index=False)

        schema = Model.generate_schema(source=temp_file.name)

    assert isinstance(schema, ModelSchema)
    assert_approx(
        json.loads(responses.calls[0].request.body),
        API_REQUEST_BODY,
        ignore_order=True,
    )


@responses.activate
def test_generate_schema_with_parquet_file() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )

    with tempfile.NamedTemporaryFile(suffix='.parquet', mode='wb') as temp_file:
        DF.to_parquet(temp_file.name, index=False)

        schema = Model.generate_schema(source=temp_file.name)

    assert isinstance(schema, ModelSchema)
    assert_approx(
        json.loads(responses.calls[0].request.body),
        API_REQUEST_BODY,
        ignore_order=True,
    )


@responses.activate
def test_generate_schema_with_rows() -> None:
    responses.post(
        url=f'{URL}/v3/generate-schema',
        json=API_RESPONSE_200,
    )

    schema = Model.generate_schema(source=DF.to_dict(orient='records'))

    assert isinstance(schema, ModelSchema)
    assert_approx(
        json.loads(responses.calls[0].request.body),
        API_REQUEST_BODY,
        ignore_order=True,
    )
