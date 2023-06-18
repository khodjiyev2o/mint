class CacheTypes:  # noqa
    registration_sms_verification = "registration_email_verification"
    forget_pass_verification = "forget_pass_verification"
    change_email_verification = "change_email_verification"


def generate_cache_key(type_, *args):
    return f"{type_}{''.join(args)}"
