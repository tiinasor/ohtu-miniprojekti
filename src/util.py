class UserInputError(Exception):
    pass

def validate_citation(content):
    if len(content) < 5:
        raise UserInputError("Citation content length must be greater than 4")

    if len(content) > 100:
        raise UserInputError("Citation content length must be smaller than 100")
