def get_schema() -> dict:
    return dict(
        type='object',
        additionalProperties=False,
        description='Execute BQ Query',
        required=['inputs', 'outputs'],
        properties=dict(
            expand_results=dict(
                type='boolean',
                default=True,
            ),
            inputs=dict(
                type='object',
                additionalProperties=False,
                required=['project_id', 'query', 'output_to_file'],
                properties=dict(
                    project_id=dict(
                        type='string',
                    ),
                    query=dict(
                        type='string',
                    ),
                    output_to_file=dict(
                        type='boolean',
                        default=True,
                    ),
                    file_pattern=dict(
                        type='string',
                    ),
                )
            ),
            outputs=dict(
                type='object',
                additionalProperties=False,
                required=['job_id', 'slot_time_ms'],
                properties=dict(
                    job_id=dict(
                        type='string',
                    ),
                    slot_time_ms=dict(
                        type='integer',
                    ),
                    files=dict(
                        type='array',
                        items=dict(
                            type='string',
                        )
                    ),
                    file=dict(
                        type='string'
                    ),
                    rows=dict(
                        type='array',
                        items=dict(
                            type='object'
                        )
                    ),
                    row=dict(
                        type='object',
                    )
                )
            )
        )
    )


def process(node_uuid, workflow_uuid, inputs, expand_results, integration):
    return dict(
        job_id='test_job_id',
        slot_time_ms=100,
        file_pattern='test_file_pattern',
    )
