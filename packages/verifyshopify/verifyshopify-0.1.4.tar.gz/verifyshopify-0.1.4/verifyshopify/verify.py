import logging
import base64
import hmac
import hashlib
from typing import AnyStr, Union

logger = logging.getLogger("ShopifyWebhookVerify")
logger.setLevel(logging.DEBUG)


def verify(
    *,
    data_bytes: bytes,
    shared_secret: Union[bytes, bytearray],
    hmac_sha256: AnyStr,
) -> bool:
    """
    Verifies the authenticity of data using HMAC (Hash-based Message Authentication Code).

    This function computes an HMAC for the given data and compares it with the HMAC provided in the header.
    It uses SHA-256 for hashing.

    Args:
        data_bytes (bytes): The data for which the HMAC is being verified.
        shared_secret (Union[bytes, AnyStr]): The secret key used for HMAC generation. It can be bytes or a string.
        hmac_sha256 (AnyStr): The base64 encoded HMAC string from the header to be compared against.

    Returns:
        bool: True if the HMAC matches, False otherwise.

    Usage:
        # The raw data received from Shopify
        raw_data_as_bytes = request.data

        # The HMAC header received from Shopify
        hmac_sha256 = request.headers.get("X-Shopify-Hmac-Sha256")

        # The secret key provided by Shopify
        secret = "xxxxxx"
        shared_secret = secret.encode("utf-8")

        verified = verify_data(
            data_bytes=raw_data_as_bytes,
            hmac_header=parsed_message.hmac_header,
            shared_secret=shared_secret,
        )
    """
    hmac_obj = hmac.new(shared_secret, data_bytes, hashlib.sha256)
    computed_hmac = hmac_obj.digest()

    try:
        received_hmac = base64.b64decode(hmac_sha256)
        verified = hmac.compare_digest(computed_hmac, received_hmac)
    except Exception as e:
        logger.error(f"Error decoding received HMAC: {e}")
        return False

    computed_hmac_b64 = base64.b64encode(computed_hmac).decode()
    logger.debug(
        f"Computed HMAC (base64): {computed_hmac_b64}, received: {hmac_sha256,}"
    )
    return verified
