"""
Utilities for semantic versioning.
"""

from packaging import version

from taktile_client.config import settings
from taktile_client.exceptions import IncompatibleVersionError


def assert_supports_version(
    *, client_version: str, server_version: str
) -> None:
    """assert_supports_version checks if two version are compatible. Raises if not

    Parameters
    ----------
    client_version : str
        client version
    server_version : str
        server version

    Raises
    ------
    IncompatibleVersionError
        If the two versions are not compatible. Error includes explanation
    """
    if settings.DEBUG:
        return

    cversion = version.Version(client_version)
    sversion = version.Version(server_version)

    supported_major_versions = {cversion.major, cversion.major - 1}

    if sversion.major not in supported_major_versions:
        raise IncompatibleVersionError(
            f"Client version {cversion} does not "
            f"support server version {sversion}. Please update."
        )

    if sversion.major == 0 and sversion.minor != 8:
        raise IncompatibleVersionError(
            f"Client version {cversion} does not "
            f"support server version {sversion}. Please update."
        )
