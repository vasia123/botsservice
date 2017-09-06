class Unauthorized(Exception):
    status_code = 401

    def __init__(self, message, status_code=None):
        Exception.__init__(self)

        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}