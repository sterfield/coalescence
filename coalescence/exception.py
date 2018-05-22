

class CoalescenceException(Exception):

    def __init__(self, msg=''):
        self.msg = msg

class NoSuchSourceException(CoalescenceException):
    pass

class NotAnElementException(CoalescenceException):
    pass

class NotAValueException(CoalescenceException):
    pass

class NoValueException(CoalescenceException):
    pass

class SerializationException(CoalescenceException):
    pass

class CoercetionException(CoalescenceException):
    pass