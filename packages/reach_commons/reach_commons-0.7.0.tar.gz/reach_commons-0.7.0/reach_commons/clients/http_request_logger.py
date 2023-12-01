import logging
import uuid

import curlify
import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


class HttpRequestLogger(HTTPAdapter):
    """
    A custom HTTPAdapter for logging details of HTTP requests and responses.
    This class logs each request and response including URL, method, headers,
    and body. It also includes a unique UUID for each request, along with
    business_id and pos_partner_name for easier query and identification.

    Attributes:
        log_level (str): Logging level ('debug', 'info', 'warning', 'error', 'critical').
        business_id (str): Identifier for the business.
        pos_partner_name (str): Name of the POS partner.

    Example of use:
        # Create a logging session with business details
        session = create_logging_session(log_level="info",
                                         business_id="12345",
                                         pos_partner_name="ExamplePOS")

        # Use the session to make requests
        response = session.get("https://httpbin.org/get", params={"test": "value"})
        # Request and response details will be logged with UUID, business_id, and pos_partner_name
    """

    def __init__(self, log_level="debug", business_id=None, pos_partner_name=None):
        super().__init__()
        self.log_level = log_level
        self.business_id = business_id
        self.pos_partner_name = pos_partner_name

    @property
    def log(self):
        return getattr(logger, self.log_level)

    def send(self, request, **kwargs):
        # Unique identifier for each request
        request_uuid = uuid.uuid4()

        # Log request details with business_id, pos_partner_name, and request_uuid
        log_message = (
            f"http_request_logger [Request UUID: {request_uuid}] "
            f"[Business ID: {self.business_id}] "
            f"[POS Partner Name: {self.pos_partner_name}]"
        )
        logger.info(f"URL: {request.url} - {log_message} ")
        logger.info(f"Method: {request.method} - {log_message}")
        logger.info(f"Headers: {request.headers} - {log_message}")
        logger.info(f"Body: {request.body} - {log_message}")

        # Send the request
        response = super(HttpRequestLogger, self).send(request, **kwargs)

        # Log response details with business_id, pos_partner_name, and request_uuid
        logger.info(f"Response Status: {response.status_code} - {log_message}")
        logger.info(f"Response Headers: {response.headers} - {log_message}")
        logger.info(f"Response Content: {response.content} - {log_message}")
        logger.info(
            f"Complete Curl: {curlify.to_curl(response.request)} - {log_message}"
        )

        return response


def create_logging_session(log_level="debug", business_id=None, pos_partner_name=None):
    session = requests.Session()
    logger_adapter = HttpRequestLogger(
        log_level=log_level, business_id=business_id, pos_partner_name=pos_partner_name
    )
    session.mount("http://", logger_adapter)
    session.mount("https://", logger_adapter)
    return session
