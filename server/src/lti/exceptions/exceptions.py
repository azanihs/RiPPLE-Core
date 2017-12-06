class OAuthException(Exception):
    def __init__(self, message):
        super(OAuthException, self).__init__(message)
        self.message = message


class LTIException(Exception):
    def __init__(self, message):
        super(LTIException, self).__init__(message)
        self.message = message
