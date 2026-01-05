## Successful Responses (2xx)

- 200 OK: Request was successful.
- 201 Created: Successful creation of a resource (typically after POST/PUT).
- 204 No Content: Request was successful, but there is no data to send back (common for "Save" or "Delete" actions).

## Client-Side Errors (4xx)

- 400 Bad Request: The server cannot process the request due to a client error (e.g., malformed syntax).
- 401 Unauthorized: The user lacks valid authentication credentials.
- 403 Forbidden: The user is authenticated but does not have permission to access the resource.
- 404 Not Found: The server cannot find the requested resource.
- 409 Conflict: This error is raised so that user can resolve the conflict and resubmit the request.
- 422 Unprocessable content: This error raises due to semantic errors. (Semantic- when syntax is correct but something is missing.)
- 429 Too Many Requests: The user has sent too many requests in a given amount of time (rate limiting).

## Server-Side Errors (5xx)

- 500 Internal Server Error: A generic error message when a more specific code isn't applicable.
- 501 Not Implemented: The server does not support the functionality required to fulfill the request.
- 502 Bad Gateway: A server acting as a gateway received an invalid response from an upstream server.
- 503 Service Unavailable: The server is temporarily down for maintenance or overloaded.
- 504 Gateway Timeout: A server acting as a gateway did not receive a timely response from an upstream server.

## Other Common Request Codes to Remember

- 301 Moved Permanently: The URL has been permanently moved to a new location.
- 302 Found (Temporary Redirect): The URL is temporarily located elsewhere.
- 405 Method Not Allowed: The request method is known by the server but is not supported for the target resource.

Link: [HTTP Response Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
