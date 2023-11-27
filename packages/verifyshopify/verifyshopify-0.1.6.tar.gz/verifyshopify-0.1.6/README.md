# Shopify Webhook Verification
This module provides a utility function to verify the authenticity of data received from Shopify webhooks. It uses HMAC (Hash-based Message Authentication Code) with SHA-256 hashing to ensure that the data has not been tampered with in transit.

## Function Description
verify is a function that computes an HMAC for the given data and compares it with the HMAC provided in the Shopify webhook header. It's designed to be a robust and secure way to validate the integrity and authenticity of the data received from Shopify.

### Arguments
- **data_bytes** (bytes): The raw data for which the HMAC is being verified.
- **shared_secret** (Union[bytes, bytearray]): The secret key used for HMAC generation.
- **hmac_sha256** (AnyStr): The base64 encoded HMAC string received in the Shopify webhook header.

### Returns
bool: Returns True if the HMAC matches, False otherwise.

### Installation
No specific installation steps required, just ensure you have Python 3.x installed.

### Usage
Here's a basic usage example:
```python
# The raw data received from Shopify
raw_data_as_bytes = request.data  # Replace with actual request data

# The HMAC header received from Shopify
hmac_sha256 = request.headers.get("X-Shopify-Hmac-Sha256")  # Replace with actual header

# The secret key provided by Shopify
shared_secret = "your_shared_secret_here".encode("utf-8")

# Perform verification
verified = verify(
    data_bytes=raw_data_as_bytes,
    hmac_sha256=hmac_sha256,
    shared_secret=shared_secret,
)

if verified:
    print("Verification successful!")
else:
    print("Verification failed!")
```
### Logging
The function uses Python's built-in logging to report its status and errors. You can configure the logging level as per your requirement.

### License
This project is licensed under the MIT License - see the LICENSE file for details.