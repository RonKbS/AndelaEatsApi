"""Error constants for the app."""


jwt_errors = {
    "NO_TOKEN": "Authorization Header is Expected",
    "NO_BEARER_MSG": "Authorization Header Must Start With Bearer",
    "SERVER_ERROR_MESSAGE": "Failed to process token",
    "EXPIRED_TOKEN_MSG": "Expired token",
    "INVALID_TOKEN_MSG": "Invalid token",
    "ISSUER_ERROR": "Issuer verification failed",
    "ALGORITHM_ERROR": "Algorithm verification failed",
    "SIGNATURE_ERROR": "Signature verification failed",
}


location_errors = {
    "IS_DIGIT": "Location Header Value is Invalid",
    "NO_LOCATION": "Location Header is Expected",
}


serialization_errors = {"INVALID_JSON": "Content-Type should be application/json"}
