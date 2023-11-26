def get_schema():
    return dict(
        type='object',
        additionalProperties=False,
        description='BigQuery integration',
        required=['extra_attributes', 'credentials'],
        properties=dict(
            extra_attributes=dict(
                type='object',
                additionalProperties=False,
                properties=dict(
                    project_id=dict(
                        type='string',
                    )
                )
            ),
            credentials=dict(
                type='object',
                additionalProperties=False,
                required=['service_account'],
                properties=dict(
                    service_account=dict(
                        type='object',
                        additionalProperties=False,
                        required=['project_id', 'private_key', 'private_key_id', 'client_email', 'client_id',
                                  'auth_uri',
                                  'token_uri', 'auth_provider_x509_cert_url', 'client_x509_cert_url',
                                  'universe_domain'],
                        properties=dict(
                            project_id=dict(
                                type='string',
                            ),
                            private_key=dict(
                                type='string',
                            ),
                            private_key_id=dict(
                                type='string',
                            ),
                            client_email=dict(
                                type='string',
                            ),
                            client_id=dict(
                                type='string',
                            ),
                            auth_uri=dict(
                                type='string',
                            ),
                            token_uri=dict(
                                type='string',
                            ),
                            auth_provider_x509_cert_url=dict(
                                type='string',
                            ),
                            client_x509_cert_url=dict(
                                type='string',
                            ),
                            universe_domain=dict(
                                type='string',
                            ),
                        )
                    ),
                )
            )

        )
    )


def connect(extra_attributes, credentials):
    from google.cloud import bigquery
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_info(credentials['service_account'])
    client = bigquery.Client(credentials=credentials)
    return dict(project_id=client.project)
