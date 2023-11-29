import click
from typing import Dict, Optional
import uuid
from pycarlo.core import Client

from montecarlodata.errors import echo_error
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors
from montecarlodata.collector.validation import CollectorValidationService
from montecarlodata.integrations.onboarding.base import BaseOnboardingService
from montecarlodata.integrations.onboarding.fields import (
    CONFLUENT_KAFKA_CLUSTER_TYPE,
    CONFLUENT_KAFKA_CONNECT_CLUSTER_TYPE,
    CONFLUENT_KAFKA_CONNECTION_TYPE,
    CONFLUENT_KAFKA_CONNECT_CONNECTION_TYPE,
    EXPECTED_ADD_STREAMING_SYSTEM_RESPONSE_FIELD,
    EXPECTED_ADD_CONFLUENT_CLUSTER_CONNECTION_RESPONSE_FIELD,
)
from montecarlodata.queries.onboarding import (
    ADD_STREAMING_SYSTEM_MUTATION,
    ADD_STREAMING_CLUSTER_CONNECTION_MUTATION,
    TEST_CONFLUENT_KAFKA_CRED_MUTATION,
    TEST_CONFLUENT_KAFKA_CONNECT_CRED_MUTATION,
)


class StreamingOnboardingService(BaseOnboardingService):
    _CONNECTION_TYPES_TO_CREDS_MUTATIONS_MAPPING = {
        CONFLUENT_KAFKA_CONNECTION_TYPE: TEST_CONFLUENT_KAFKA_CRED_MUTATION,
        CONFLUENT_KAFKA_CONNECT_CONNECTION_TYPE: TEST_CONFLUENT_KAFKA_CONNECT_CRED_MUTATION,
    }

    _CONNECTION_TYPES_TO_CLUSTER_TYPE_MAPPING = {
        CONFLUENT_KAFKA_CONNECTION_TYPE: CONFLUENT_KAFKA_CLUSTER_TYPE,
        CONFLUENT_KAFKA_CONNECT_CONNECTION_TYPE: CONFLUENT_KAFKA_CONNECT_CLUSTER_TYPE,
    }

    def __init__(self, config: Config, mc_client: Client, **kwargs):
        super().__init__(config, **kwargs)
        self._validation_service = CollectorValidationService(
            config=config,
            mc_client=mc_client,
            user_service=self._user_service,
            request_wrapper=self._request_wrapper,
        )

    @manage_errors
    def create_streaming_system(
        self,
        streaming_system_type: str,
        streaming_system_name: str,
        dc_id: Optional[str] = None,
    ) -> None:
        """
        Creates a confluent system.
        """
        response = self._request_wrapper.make_request_v2(
            query=ADD_STREAMING_SYSTEM_MUTATION,
            operation=EXPECTED_ADD_STREAMING_SYSTEM_RESPONSE_FIELD,
            variables=dict(
                streaming_system_type=streaming_system_type,
                streaming_system_name=streaming_system_name,
                dc_id=dc_id,
            ),
        )
        streaming_system = response.data.streamingSystem
        click.echo(
            f"Successfully created the {streaming_system.type} streaming system "
            f"{streaming_system.name} with uuid: {streaming_system.uuid}."
        )

    @manage_errors
    def test_new_confluent_kafka_credentials(
        self,
        cluster: str,
        api_key: str,
        secret: str,
        url: str,
        dc_id: Optional[uuid.UUID] = None,
    ) -> str:

        return self._validation_service.test_new_credentials(
            dc_id=dc_id,
            connection_type=CONFLUENT_KAFKA_CONNECTION_TYPE,
            cluster=cluster,
            api_key=api_key,
            secret=secret,
            url=url,
        )

    @manage_errors
    def test_new_confluent_kafka_connect_credentials(
        self,
        confluent_env: str,
        cluster: str,
        api_key: str,
        secret: str,
        url: Optional[str] = None,
        dc_id: Optional[uuid.UUID] = None,
    ) -> str:
        return self._validation_service.test_new_credentials(
            dc_id=dc_id,
            connection_type=CONFLUENT_KAFKA_CONNECT_CONNECTION_TYPE,
            confluent_env=confluent_env,
            cluster=cluster,
            api_key=api_key,
            secret=secret,
            url=url,
        )

    @manage_errors
    def onboard_confluent_cluster_connection(self, **kwargs) -> None:
        connection_type = kwargs.get("connection_type")
        if (
            connection_type
            not in self._CONNECTION_TYPES_TO_CREDS_MUTATIONS_MAPPING.keys()
        ):
            echo_error("Not supported streaming connection type")
            click.Abort()

        credential_key = kwargs.get("key")
        if not credential_key:
            credential_key = self._test_and_generate_credential_key(
                connection_type=connection_type, params=kwargs
            )
            if credential_key:
                kwargs["key"] = credential_key
            else:
                # credentials testing fail or user doesn't want to continue
                click.Abort()

        if not kwargs.get("mc_cluster_id"):
            # for new cluster, we'll add the cluster type here.
            kwargs["new_cluster_type"] = self._CONNECTION_TYPES_TO_CLUSTER_TYPE_MAPPING[
                connection_type
            ]

        response = self._request_wrapper.make_request_v2(
            query=ADD_STREAMING_CLUSTER_CONNECTION_MUTATION,
            operation=EXPECTED_ADD_CONFLUENT_CLUSTER_CONNECTION_RESPONSE_FIELD,
            variables=kwargs,
        )

        connection = response.data.connection
        click.echo(
            f"Successfully created the {connection.type} connection {connection.uuid} for cluster "
            f"{connection.streamingCluster.uuid}, in streaming system "
            f"{connection.streamingCluster.streamingSystemUuid}."
        )

    def _test_and_generate_credential_key(
        self, connection_type: str, params: Dict
    ) -> str:
        parameters = {
            "cluster": params.get("new_cluster_id"),
            "api_key": params.get("api_key"),
            "secret": params.get("secret"),
        }
        if connection_type == CONFLUENT_KAFKA_CONNECTION_TYPE:
            parameters["url"] = params.get("url")
        elif connection_type == CONFLUENT_KAFKA_CONNECT_CONNECTION_TYPE:
            parameters["confluent_env"] = params.get("confluent_env")
            if "url" in params:
                parameters["url"] = params.get("url")
        else:
            click.echo(f"Not supported connection type {connection_type}")

        return self._validation_service.test_new_credentials(
            connection_type=connection_type, dc_id=params.get("dc_id"), **parameters
        )
