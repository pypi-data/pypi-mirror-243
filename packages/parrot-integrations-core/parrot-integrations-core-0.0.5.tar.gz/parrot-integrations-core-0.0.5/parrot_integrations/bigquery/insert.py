from jsonpath_ng.ext import parse as ng_parse


def get_schema():
    return dict(
        type='object',
        additionalProperties=False,
        description='Insert Row into BigQuery Table',
        required=['inputs', 'outputs'],
        properties=dict(
            inputs=dict(
                type='object',
                additionalProperties=False,
                required=['project_id', 'dataset_id', 'table_id', 'columns'],
                properties=dict(
                    project_id=dict(
                        type='object',
                        additionalProperties=False,
                        properties=dict(
                            oneOf=[
                                dict(
                                    path=dict(
                                        type='string',
                                        minLength=1,
                                    ),
                                    default=dict(
                                        type='string',
                                    )
                                ),
                                dict(
                                    value='string',
                                    minLength=1,
                                )
                            ]
                        ),
                    ),
                    dataset_id=dict(
                        type='object',
                        additionalProperties=False,
                        properties=dict(
                            oneOf=[
                                dict(
                                    path=dict(
                                        type='string',
                                        minLength=1,
                                    ),
                                    default=dict(
                                        type='string',
                                    )
                                ),
                                dict(
                                    value='string',
                                    minLength=1,
                                )
                            ]
                        ),
                    ),
                    table_id=dict(
                        type='object',
                        additionalProperties=False,
                        properties=dict(
                            oneOf=[
                                dict(
                                    path=dict(
                                        type='string',
                                        minLength=1,
                                    ),
                                    default=dict(
                                        type='string',
                                    )
                                ),
                                dict(
                                    value='string',
                                    minLength=1,
                                )
                            ]
                        ),
                    ),
                    records=dict(
                        type='object',
                        additionalProperties=False,
                        properties=dict(
                            path=dict(
                                type='string',
                            )
                        )
                    ),
                    table_schema=dict(
                        type='array',
                        minItems=1,
                        items=dict(
                            type='object',
                            additionalProperties=False,
                            required=['name', 'type'],
                            properties=dict(
                                name=dict(
                                    type='string',
                                ),
                                type=dict(
                                    type='string',
                                    enum=['STRING', 'INTEGER', 'NUMERIC', 'BOOLEAN', 'TIMESTAMP']
                                ),
                                path=dict(
                                    type='string',
                                ),
                                value=dict(
                                    type=['string', 'integer', 'number', 'boolean', 'null'],
                                ),
                                default=dict(
                                    type=['string', 'integer', 'number', 'boolean', 'null'],
                                )
                            )
                        )
                    )
                )
            ),
            outputs=dict(
                type='object',
                additionalProperties=False,
                required=['row_id'],
                properties=dict(
                    row_id=dict(
                        type='string',
                    ),
                    inserted_ts=dict(
                        type='integer',
                    )
                )
            ),
        )
    )


def process(workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, inputs, integration,
            **kwargs):
    from google.cloud import bigquery
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_info(integration['credentials']['service_account'])
    client = bigquery.Client(credentials=credentials)
    table = client.get_table(
        table='{project_id}.{dataset_id}.{table_id}'.format(
            project_id=inputs['project_id'],
            dataset_id=inputs['dataset_id'],
            table_id=inputs['table_id'],
        )
    )
    client.insert_rows_json(
        table=table,
        json_rows=format_rows(data=inputs['records'], workflow_uuid=workflow_uuid, account_uuid=account_uuid,
                              node_uuid=node_uuid, trigger_uuid=trigger_uuid, ingested_ts=ingested_ts,
                              processed_ts=processed_ts, schema=inputs['table_schema'])
    )
    return dict(
        job_id='test_job_id',
        slot_time_ms=100,
        file_pattern='test_file_pattern',
    )


def format_rows(data, workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, schema):
    if not isinstance(data, list):
        data = [data]
    rows = list()
    for record in data:
        row = dict(
            account_uuid=account_uuid,
            workflow_uuid=workflow_uuid,
            node_uuid=node_uuid,
            trigger_uuid=trigger_uuid,
            ingested_ts=ingested_ts,
            processed_ts=processed_ts,
        )
        for column in schema:
            value = None
            if 'path' in column:
                parser = ng_parse(column['path'])
                value = [i.value for i in parser.find(record)]
                if len(value) == 0:
                    value = None
                elif len(value) == 1:
                    value = value[0]
            elif 'value' in column:
                value = column['value']
            if value is None and 'default' in column:
                value = column['default']
            row[column['name']] = value
        rows.append(
            record
        )
    return rows
