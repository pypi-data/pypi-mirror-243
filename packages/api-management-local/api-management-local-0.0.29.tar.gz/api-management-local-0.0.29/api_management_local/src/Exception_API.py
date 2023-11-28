# define Python user-defined exceptions
class PassedTheHardLimitException(Exception):
    "Raised when the input value is less than 18"
    pass

class ApiTypeIsNotExistException(Exception): #v
    " Api_Type_Id is not exsit in your table view"
    pass

class ApiTypeDisabledException(Exception): #v
    " Api_Type_Id is disabled"
    pass

class NotEnoughStarsForActivityException(Exception):#v
    " Not enough stars for action"
    pass
