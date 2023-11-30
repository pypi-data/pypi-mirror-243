import cx_Oracle

from sageodata_db.utils import get_logger


logger = get_logger()

PROD_SERVER = "pirsapd07.pirsa.sa.gov.au"
TEST_SERVER = "PIRZAPD08.pirsa.sa.gov.au"
PORT = 1521


def normalize_service_name(name: str) -> str:
    """Ensure consistent SA Geodata service name.

    Args:
        service_name (str): database service name e.g. "DMEP.World", "DMET.World",
            or "DMED.World". Can also pass "prod", "test", or "dev".

    Returns the proper service name e.g. DMEP.WORLD for prod.

    """
    if name.lower() in ("prod", "production"):
        name = "DMEP.WORLD"
    elif name.lower() in ("test", "qa"):
        name = "DMET.WORLD"
    elif name.lower() in ("dev", "development"):
        name = "DMED.WORLD"
    if not name.upper() in ("DMEP.WORLD", "DMET.WORLD", "DMED.WORLD"):
        raise KeyError(
            "name must be either:\n"
            " - prod, DMEP.World\n"
            " - QA, test, DMET.World\n"
            " - dev, DMED.WORLD"
        )
    return name


def find_appropriate_server(service_name: str) -> str:
    """Find the server that each service name lives on. See PROD_SERVER
    and TEST_SERVER.

    Args:
        service_name (str): one of "DMET.WORLD", "DMED.WORLD", or "DMEP.WORLD".

    Returns: str (server name).

    """
    if service_name.upper() == "DMET.WORLD":
        server = TEST_SERVER
    elif service_name.upper() == "DMED.WORLD":
        server = TEST_SERVER
    elif service_name.upper() == "DMEP.WORLD":
        server = PROD_SERVER
    else:
        raise KeyError(
            "service_name must be either DMEP.WORLD, DMET.WORLD, or DMED.WORLD"
        )
    return server


def makedsn(service_name="DMEP.WORLD", server=None, port=PORT):
    """Get the appropriate Oracle DSN.

    Args:
        service_name (str): database service name e.g. "DMEP.WORLD", "DMET.WORLD",
            or "DMED.WORLD". This goes to :func:`sageodata_db.normalize_service_name`
            first so you can also pass "prod", "test", or "dev".
        server (str, optional): server address
        port (int, optional): port

    For example, to get the production database:

        >>> from sageodata_db import makedsn
        >>> makedsn("prod")
        '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=pirsapd07.pirsa.sa.gov.au)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=DMEP.World)))'

    """
    service_name = normalize_service_name(service_name)
    if server is None:
        server = find_appropriate_server(service_name)
    return cx_Oracle.makedsn(server, port, service_name=service_name)


def make_connection_string(service_name="DMEP.WORLD", server=None, port=PORT):
    """Get the appropriate cx_Oracle connection string.

    Args:
        service_name (str): database service name e.g. "DMEP.WORLD", "DMET.WORLD",
            or "DMED.WORLD". This goes to :func:`sageodata_db.normalize_service_name`
            first so you can also pass "prod", "test", or "dev".
        server (str, optional): server address
        port (int, optional): port

    For example, to get the production database:

        >>> from sageodata_db import makedsn
        >>> makedsn("prod")
        '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=pirsapd07.pirsa.sa.gov.au)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=DMEP.World)))'

    """
    service_name = normalize_service_name(service_name)
    if server is None:
        server = find_appropriate_server(service_name)
    return "{}:{}/{}".format(server, port, service_name)
