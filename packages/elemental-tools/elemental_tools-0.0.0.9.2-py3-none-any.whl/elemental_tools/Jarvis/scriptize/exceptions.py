from elemental_tools.Jarvis.scriptize.config import logger


class ScriptModuleMissing:

    def __init__(self, title):
        print(f'Script module missing when validating: {title}')


class ParameterMissing(Exception):

    def __init__(self, title):
        Exception.__init__(self, f"The argument {title} is missing.")


class SettingMissing(Exception):

    def __init__(self, title):
        Exception.__init__(self, f"The Setting: {title} cannot be found on the database\n"
                                 f"If you want to create a custom Setting, you must add to your code:\n\t"
                                 f"""from elemental_tools.Jarvis.scriptize.api.settings import SettingsController

                                    _settings = SettingsController()
                                    _settings.create()"""
                                 f"If it was not your intent, try to run: python3 -m elemental_tools.Jarvis.install")


class ThreadTimeout(Exception):
    pass


class ThreadLimitExceeded(Exception):
    pass


class SkipExecution:

    def __init__(self, msg: str = "", app: str = None):
        logger('skip-execution', msg, app_name='scripts')

