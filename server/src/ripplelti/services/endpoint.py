# -*- coding: utf-8 -*-
"""
Re-written from the following URL to not suppress errors
https://github.com/idan/oauthlib/blob/master/oauthlib/oauth1/rfc5849/endpoints/signature_only.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module is an implementation of the signing logic of OAuth 1.0 RFC 5849.
"""
from __future__ import absolute_import, unicode_literals

from ..exceptions import OAuthException

from oauthlib.oauth1 import OAuth1Error
from oauthlib.oauth1 import SignatureOnlyEndpoint


class SignatureEndpoint(SignatureOnlyEndpoint):

    """An endpoint only responsible for verifying an oauth signature."""

    def validate_request(self, uri, http_method='GET',
                         body=None, headers=None):
        """Validate a signed OAuth request.
        :param uri: The full URI of the token request.
        :param http_method: A valid HTTP verb, i.e. GET, POST, PUT, HEAD, etc.
        :param body: The request body as a string.
        :param headers: The request headers as a dict.
        :returns: A tuple of 2 elements.
                  1. True if valid, False otherwise.
                  2. An oauthlib.common.Request object.
        """
        try:
            request = self._create_request(uri, http_method, body, headers)
        except OAuth1Error as err:
            raise OAuthException("Error validating request, %s" % err)

        try:
            self._check_transport_security(request)
            self._check_mandatory_parameters(request)
        except OAuth1Error as err:
            raise OAuthException("Could not validate request, %s" % err)

        if not self.request_validator.validate_timestamp_and_nonce(
                request.client_key, request.timestamp, request.nonce, request):
            raise OAuthException("Timestamp / nonce invalid")

        # The server SHOULD return a 401 (Unauthorized) status code when
        # receiving a request with invalid client credentials.
        # Note: This is postponed in order to avoid timing attacks, instead
        # a dummy client is assigned and used to maintain near constant
        # time request verification.
        #
        # Note that early exit would enable client enumeration
        valid_client = self.request_validator.validate_client_key(
            request.client_key, request)
        if not valid_client:
            request.client_key = self.request_validator.dummy_client

        valid_signature = self._check_signature(request)

        # log the results to the validator_log
        # this lets us handle internal reporting and analysis
        request.validator_log['client'] = valid_client
        request.validator_log['signature'] = valid_signature

        # We delay checking validity until the very end, using dummy values for
        # calculations and fetching secrets/keys to ensure the flow of every
        # request remains almost identical regardless of whether valid values
        # have been supplied. This ensures near constant time execution and
        # prevents malicious users from guessing sensitive information
        v = all((valid_client, valid_signature))
        if not valid_client:
            raise OAuthException(
                "Could not validate client key: %s" % request.client_key,)
        if not valid_signature:
            raise OAuthException("Could not validate signature")
        return v, request
