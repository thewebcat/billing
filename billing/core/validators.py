from jsonschema import draft4_format_checker


def init_validators():

    @draft4_format_checker.checks('customdate')
    def is_custom_date(val):
        from datetime import datetime
        try:
            _ = datetime.strptime(val, '%Y-%m-%d') # NOQA
        except ValueError:
            return False
        return True
