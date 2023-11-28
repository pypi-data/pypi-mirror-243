import os


class EnvReader:

    @staticmethod
    def read_bool_env(key: str):
        bool_prev = os.environ.get(key)
        bool_value = None
        if bool_prev is not None:
            bool_value = bool_prev.lower() in ("true", "1", "yes")
        return bool_value

