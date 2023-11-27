########
# Copyright (c) 2014-2022 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cfy_lint.yamllint_ext import LintProblem
from cfy_lint.yamllint_ext.rules import constants
from cfy_lint.yamllint_ext.generators import CfyNode
from cfy_lint.yamllint_ext.utils import (
    process_relevant_tokens,
    check_node_imported,
    recurse_get_readable_object,
    context as ctx
    )
from cfy_lint.yamllint_ext.rules.node_templates import (
    remove_node_type_from_context
)

VALUES = []

ID = 'node_types'
TYPE = 'token'
CONF = {'allowed-values': list(VALUES), 'check-keys': bool}
DEFAULT = {'allowed-values': ['true', 'false'], 'check-keys': True}


@process_relevant_tokens(CfyNode, 'node_types')
def check(token=None, skip_suggestions=None, **_):
    for node_type in token.node.value:
        types = get_type_and_check_dsl(node_type)
        dsl = ctx.get("dsl_version")
        for value in types:
            if value not in constants.INPUTS_BY_DSL.get(dsl, []):
                yield LintProblem(
                    token.line,
                    None,
                    'Type {} is not supported by DSL {}.'.format(value, dsl)
                )
        if check_node_imported(node_type[0].value):
            yield from node_type_follows_naming_conventions(
                node_type[0].value, token.line, skip_suggestions)
    remove_node_type_from_context(node_type)


def get_values_by_key_type(dictionary):
    values = []
    if 'type' in dictionary:
        values.append(dictionary['type'])
    for value in dictionary.values():
        if isinstance(value, dict):
            nested_values = get_values_by_key_type(value)
            values.extend(nested_values)
    return values


def get_type_and_check_dsl(node_type):
    node_type = recurse_get_readable_object(node_type)
    return get_values_by_key_type(node_type)


def node_type_follows_naming_conventions(value, line, skip_suggestions=None):
    suggestions = 'node_templates' in skip_suggestions
    split_node_type = value.split('.')
    last_key = split_node_type.pop()
    if not {'cloudify', 'nodes'} <= set(split_node_type):
        yield LintProblem(
            line,
            None,
            "node types should follow naming convention cloudify.nodes.*: "
            "{}".format(value))
    if not good_camel_case(last_key, split_node_type) and not suggestions:
        new_value = '.'.join(
            [k.lower() for k in split_node_type]) + '.{}'.format(last_key)
        yield LintProblem(
            line,
            None,
            "incorrect camel case {}. Suggested: {} ".format(value, new_value))


def good_camel_case(last_key, split_node_type):
    if not last_key[0].isupper():
        return False
    for key in split_node_type:
        if key[0].isupper():
            return False
    return True
