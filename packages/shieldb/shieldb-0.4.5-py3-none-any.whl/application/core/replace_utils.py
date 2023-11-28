from application.core.enums import Actions

class ReplaceUtils:
    def __init__(self):
        self.replace_password = ReplaceUtils.replace_password()
        self.replace_email = ReplaceUtils.replace_email()
        self.replace_credit_card_number = ReplaceUtils.replace_credit_card_number()
        self.replace_phone_number = ReplaceUtils.replace_phone_number()

    @staticmethod
    def replace_email(match):
        email = match.group(0)
        if len(email) > 2:
            parts = email.split("@")
            username = parts[0]
            new_email = email[0] + Actions.MASK_CHAR.value * (len(username) - 2) + username[-1] + '@' + parts[1]
            return new_email
        else:

            return email

    @staticmethod
    def replace_phone_number(match):
        phone = match.group(0)
        response = phone[:-4] + (4*Actions.MASK_CHAR.value)
        return response

    @staticmethod
    def replace_credit_card_number(match):
        credit_card_number = match.group(0)
        response = credit_card_number[:4] + Actions.MASK_CHAR.value * (len(credit_card_number) - 4)
        return response

    @staticmethod
    def replace_password(match):
        username = match.group(1)
        if len(match.group(2)) > 5:
            response = username + (Actions.MASK_CHAR.value * len(match.group(2)))
        else:
            response = f"{username}{match.group(2)}"
        return response
