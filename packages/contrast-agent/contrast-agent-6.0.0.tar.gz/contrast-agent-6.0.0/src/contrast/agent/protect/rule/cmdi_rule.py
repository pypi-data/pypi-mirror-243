# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import re

from contrast.agent.protect.rule.base_rule import BaseRule


class CmdInjection(BaseRule):
    """
    Command Injection Protection rule
    """

    RULE_NAME = "cmd-injection"

    BIN_SH_C = "/bin/sh-c"

    START_IDX = "start_idx"
    END_IDX = "end_idx"

    def find_attack(self, candidate_string=None, **kwargs):
        command_string = str(candidate_string) if candidate_string else None

        return super().find_attack(command_string, **kwargs)

    def build_sample(self, evaluation, command, **kwargs):
        sample = self.build_base_sample(evaluation)

        if command is not None:
            sample.details["command"] = command

        if self.START_IDX in kwargs or self.END_IDX in kwargs:
            sample.details["startIndex"] = kwargs.get(self.START_IDX, 0)
            sample.details["endIndex"] = kwargs.get(self.END_IDX, 0)
        elif command is not None:
            search_value = evaluation.value

            match = re.search(search_value, command, re.IGNORECASE)

            if match:
                sample.details["startIndex"] = match.start()
                sample.details["endIndex"] = match.end()

        return sample

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(method=patch_policy.method_name, original_command=user_input)

    def skip_protect_analysis(self, user_input, args, kwargs):
        """
        cmdi rule supports list user input as well as str and bytes
        Do not skip protect analysis if user input is a  populated list
        """
        if isinstance(user_input, list) and user_input:
            return False

        return super().skip_protect_analysis(user_input, args, kwargs)

    def convert_input(self, user_input):
        if isinstance(user_input, list):
            user_input = " ".join(user_input)

        return super().convert_input(user_input)

    def infilter(self, match_string, **kwargs):
        # TODO: PYT-3088
        #  deserialization_rule = Settings().protect_rules[Deserialization.RULE_NAME]
        #  deserialization_rule.check_for_deserialization()
        pass

        super().infilter(match_string, **kwargs)
