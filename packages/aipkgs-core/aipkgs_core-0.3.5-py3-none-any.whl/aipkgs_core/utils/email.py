from email_validator import validate_email, EmailNotValidError


def is_email_valid(email: str) -> (bool, str):
  try:
    valid = validate_email(email)

    email = valid.email
    return True
  except EmailNotValidError as e:
    return False

