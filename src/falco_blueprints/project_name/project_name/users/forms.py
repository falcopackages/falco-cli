from allauth.account.forms import SignupForm


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    # This prevent django-fastdev from raising an error when accessing the signup page
    clean_username = None
