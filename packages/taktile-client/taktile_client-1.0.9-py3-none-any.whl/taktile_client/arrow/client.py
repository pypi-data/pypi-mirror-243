"""
Client for talking to arrow endpoints
"""
import logging
import typing as t

# pylint: disable-next=no-name-in-module
from pyarrow._flight import (  # type: ignore
    ClientAuthReader,
    ClientAuthSender,
    FlightServerError,
)
from pyarrow.flight import (  # type: ignore
    ClientAuthHandler,
    FlightClient,
    Ticket,
)
from taktile_types.schemas.deployment.endpoint import (
    InfoEndpointResponseModelFlight,
)

from taktile_client.arrow.serialize import deserialize
from taktile_client.arrow.utils import load_certs
from taktile_client.client import Client
from taktile_client.config import version as cversion
from taktile_client.version import assert_supports_version

from ..config import settings
from .endpoint import ArrowEndpoints

logger = logging.getLogger(__name__)


class ApiKeyClientAuthHandler(ClientAuthHandler):  # type: ignore
    """Auth Handler"""

    def __init__(self, api_key: str):
        super().__init__()
        self._api_key = api_key

    def authenticate(
        self, outgoing: ClientAuthSender, incoming: ClientAuthReader
    ) -> None:
        """authenticate"""
        outgoing.write(self._api_key)
        self._api_key = incoming.read()

    def get_token(self) -> str:
        """get_token"""
        return self._api_key


class ArrowClient(Client[ArrowEndpoints]):
    """
    Arrow client for talking to models deployed with Taktile.
    """

    def _url_from_host(self, host: str) -> str:
        if settings.DEBUG:
            return f"grpc://{host}:5005"
        return f"grpc+tls://{host}:5005"

    def _initalize_endpoints(
        self, url: str, api_key: t.Optional[str]
    ) -> ArrowEndpoints:

        certs = load_certs()
        logger.debug("Performing authentication request against %s", url)
        client = FlightClient(location=url, tls_root_certs=certs)
        if api_key:
            client.authenticate(ApiKeyClientAuthHandler(api_key=api_key))
        actions = client.list_actions()
        self.info = _get_info(client)
        if self.info:
            assert_supports_version(
                client_version=cversion,
                server_version=self.info.taktile_cli,
            )
        return ArrowEndpoints(client=client, actions=actions)


def _get_info(
    client: FlightClient,
) -> t.Union[InfoEndpointResponseModelFlight, None]:
    try:
        return InfoEndpointResponseModelFlight(
            **deserialize(client.do_get(Ticket("__info")).read_all())
        )
    except FlightServerError as err:
        logger.warning("Failed to get info %s", repr(err))
        return None
