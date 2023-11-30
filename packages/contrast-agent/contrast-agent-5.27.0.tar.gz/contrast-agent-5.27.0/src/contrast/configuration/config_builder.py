# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.utils.configuration_utils import get_env_key
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")

ENV_PREFIX = "CONTRAST"


class ConfigBuilder(object):
    def __init__(self):
        self.default_options = []

    def build(self, config, yaml_config, yaml_filename):
        """
        Given a dict config, iterate over the default_options and check if
        the corresponding config key/value should be either :
        1. replaced by an existing env var
        2. keep existing config key/val but type-cast the value
        3. add a new key/default_value to the config

        :param config: dict config
        :return: str if error was set, config dict is updated pass by reference
        """
        error = None
        for option in self.default_options:
            option_name = option.canonical_name
            type_cast = option.type_cast

            underscore_alt = self._underscore_alternative(option_name)
            env_override = get_env_key(underscore_alt)
            if env_override is not None:
                try:
                    option.env_value = type_cast(env_override)
                    option.name = underscore_alt
                except Exception as e:
                    logger.exception("Failed to initialize config")
                    if error is None:
                        error = f"Invalid value on {option.canonical_name} - {e}"
            if yaml_config:
                file_override = yaml_config.get(option_name, None)
                if file_override is not None:
                    try:
                        option.file_value = type_cast(file_override)
                        option.file_source = yaml_filename
                    except Exception as e:
                        logger.exception("Failed to initialize config")
                        if error is None:
                            error = f"Invalid value on {option_name} - {e}"
            config[option_name] = option
        return error

    def _underscore_alternative(self, key):
        return "__".join([x for x in [ENV_PREFIX, key.replace(".", "__")] if x]).upper()
