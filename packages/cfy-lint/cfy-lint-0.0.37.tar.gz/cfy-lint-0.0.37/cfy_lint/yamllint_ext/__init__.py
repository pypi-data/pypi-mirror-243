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

import os
import re

from yamllint import parser
from cfy_lint.yamllint_ext.constants import (
    UNUSED_INPUTS, UNUSED_IMPORT_CTX)
from cfy_lint.yamllint_ext.generators import (
    CfyNode,
    CfyToken,
    YamlParserLintProblem,
    token_or_comment_or_line_generator,
)
from cfy_lint.yamllint_ext.overrides import (
    LintProblem,
    spaces_after,
    spaces_before,
    get_syntax_error
)
from cfy_lint.yamllint_ext.utils import (
    context,
    setup_types,
    update_model,
    setup_node_templates,
    add_severity
)
from cfy_lint.yamllint_ext.autofix.utils import build_diff_lines
from cfy_lint.yamllint_ext.autofix import fix_problem
from cfy_lint.yamllint_ext.rules.inputs import ID as input_rule
from cfy_lint.yamllint_ext.rules.imports import ID as import_rule
from cfy_lint.yamllint_ext.autofix.add_label import fix_add_label
from cfy_lint.yamllint_ext.autofix.empty_lines import fix_empty_lines

PROBLEM_LEVELS = {
    0: None,
    1: 'warning',
    2: 'error',
    None: 0,
    'warning': 1,
    'error': 2,
}


def get_cosmetic_problems(buffer,
                          conf,
                          filepath,
                          base_path=None,
                          skip_suggestions=None):

    setup_types(buffer, base_path=base_path)

    rules = conf.enabled_rules(filepath)

    # Split token rules from line rules
    token_rules = [r for r in rules if r.TYPE == 'token']
    comment_rules = [r for r in rules if r.TYPE == 'comment']
    line_rules = [r for r in rules if r.TYPE == 'line']

    for rule in token_rules:
        context[rule.ID] = {}

    class DisableDirective:
        def __init__(self):
            self.rules = set()
            self.all_rules = {r.ID for r in rules}

        def process_comment(self, comment):
            try:
                comment = str(comment)
            except UnicodeError:
                return  # this certainly wasn't a yamllint directive comment

            if re.match(r'^# yamllint disable( rule:\S+)*\s*$', comment):
                items = comment[18:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

            elif re.match(r'^# yamllint enable( rule:\S+)*\s*$', comment):
                items = comment[17:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules.clear()
                else:
                    for id in rules:
                        self.rules.discard(id)

        def is_disabled_by_directive(self, problem):
            return problem.rule in self.rules

    class DisableLineDirective(DisableDirective):
        def process_comment(self, comment):
            try:
                comment = str(comment)
            except UnicodeError:
                return  # this certainly wasn't a yamllint directive comment

            if re.match(r'^# yamllint disable-line( rule:\S+)*\s*$', comment):
                items = comment[23:].rstrip().split(' ')
                rules = [item[5:] for item in items][1:]
                if len(rules) == 0:
                    self.rules = self.all_rules.copy()
                else:
                    for id in rules:
                        if id in self.all_rules:
                            self.rules.add(id)

    # Use a cache to store problems and flush it only when a end of line is
    # found. This allows the use of yamllint directive to disable some rules on
    # some lines.
    cache = []
    disabled = DisableDirective()
    disabled_for_line = DisableLineDirective()
    disabled_for_next_line = DisableLineDirective()

    for elem in token_or_comment_or_line_generator(buffer):
        if isinstance(elem, YamlParserLintProblem):
            yield LintProblem(elem.line, elem. column, elem.desc)

        if isinstance(elem, CfyNode):
            setup_node_templates(elem)
            for rule in token_rules:
                rule_conf = conf.rules[rule.ID]
                elem.blueprint_path = base_path
                try:
                    problems = rule.check(
                        conf=rule_conf,
                        token=elem,
                        context=context[rule.ID],
                        node_types=context.get('imported_node_types', {}),
                        skip_suggestions=skip_suggestions)
                except TypeError:
                    continue
                else:
                    for problem in problems:
                        problem.rule = rule.ID
                        problem.level = rule_conf['level']
                        cache.append(problem)

        elif isinstance(elem, CfyToken):
            update_model(elem)
            for rule in token_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                problems = rule.check(rule_conf,
                                      elem.curr,
                                      elem.prev,
                                      elem.after,
                                      elem.nextnext,
                                      context[rule.ID])
                for problem in problems:
                    problem.rule = rule.ID
                    if problem.rule in ['truthy']:
                        problem.fixable = True
                    problem.level = rule_conf['level']
                    cache.append(problem)

        elif isinstance(elem, parser.Comment):
            for rule in comment_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    problem.level = rule_conf['level']
                    cache.append(problem)

            disabled.process_comment(elem)
            if elem.is_inline():
                disabled_for_line.process_comment(elem)
            else:
                disabled_for_next_line.process_comment(elem)

        elif isinstance(elem, parser.Line):
            for rule in line_rules:
                if hasattr(rule, 'LintProblem'):
                    rule.LintProblem = LintProblem
                if hasattr(rule, 'spaces_before'):
                    rule.spaces_before = spaces_before
                if hasattr(rule, 'spaces_after'):
                    rule.spaces_after = spaces_after
                rule_conf = conf.rules[rule.ID]
                for problem in rule.check(rule_conf, elem):
                    problem.rule = rule.ID
                    if problem.rule in ['trailing-spaces', 'empty-lines']:
                        problem.fixable = True
                    problem.level = rule_conf['level']
                    cache.append(problem)

    # if this runs with the other loop, we will not have a chance
    # to check usage of plugins in the blueprint, before
    # it is reported.
    for import_item, problem in context.get(
            'post_processing_problems', {}).items():
        if import_item in context[UNUSED_IMPORT_CTX]:
            problem.rule = import_rule
            problem.level = 'error'
            cache.append(problem)

    for _, problem in context.get(UNUSED_INPUTS, {}).items():
        problem.rule = input_rule
        problem.level = 'error'
        cache.append(problem)

    # This is the last token/comment/line of this line, let's flush the
    # problems found (but filter them according to the directives)
    for problem in cache:
        if not (disabled_for_line.is_disabled_by_directive(problem) or
                disabled.is_disabled_by_directive(problem)):
            yield problem

    disabled_for_line = disabled_for_next_line
    disabled_for_next_line = DisableLineDirective()
    cache = []


def _run(buffer,
         conf,
         filepath,
         base_path=None,
         input_file=None,
         skip_suggestions=None,
         fix=None):
    fix = fix or []

    assert hasattr(buffer, '__getitem__'), \
        '_run() argument must be a buffer, not a stream'

    first_line = next(parser.line_generator(buffer)).content
    if re.match(r'^#\s*yamllint disable-file\s*$', first_line):
        return

    # If the document contains a syntax error, save it and yield it at the
    # right line
    syntax_error = get_syntax_error(buffer)

    problems = list(get_cosmetic_problems(buffer,
                                          conf,
                                          filepath,
                                          base_path,
                                          skip_suggestions))

    sorted_problems = sorted(problems, key=lambda x: x.line)
    add_label = False
    extra_empty_line = False
    for problem in sorted_problems:
        if not problem.severity:
            add_severity(problem)

    for problem in sorted_problems:

        problem.fixes = fix
        # Insert the syntax error (if any) at the right place...

        if (syntax_error and syntax_error.line <= problem.line and
                syntax_error.column <= problem.column):
            yield syntax_error

            # If there is already a yamllint error at the same place, discard
            # it as it is probably redundant (and maybe it's just a 'warning',
            # in which case the script won't even exit with a failure status).
            if (syntax_error.line == problem.line and
                    syntax_error.column == problem.column):
                syntax_error = None
                continue

            syntax_error = None

        if problem.fix:
            input_file_path = os.path.abspath(input_file)
            problem.file = input_file_path

            if problem.rule == 'inputs' and \
                    'is missing a display_label' in problem.message:
                add_label = True
                problem.fixed = True
            if problem.rule == 'empty-lines':
                extra_empty_line = True
                problem.fixed = True
            fix_problem(problem)

        if not fix:
            yield problem

    if add_label:
        fix_add_label(sorted_problems)

    # this needs to be separated from the rest of the auto fix functions since
    # it changes the line numbers of the entire file, so we do it once all
    # other tasks are done
    if extra_empty_line:
        fix_empty_lines(problem)

    if context['line_diff'] or context['add_label']:
        build_diff_lines()

    # Fix the lines in the error message according to the dictionary we created
    index = 0
    lines = list(context['line_diff'].keys())
    values = list(context['line_diff'].values())
    len_lines = len(lines)
    if lines:
        for problem in sorted_problems:
            if problem.fixed:
                continue
            if problem.line > lines[index]:
                while (index + 1 < len_lines and
                       problem.line not in range(
                           lines[index],
                           lines[index + 1])):
                    index += 1
                problem.update_line = problem.line + values[index]

            if not problem.fixed:
                yield problem

    if syntax_error:
        yield syntax_error


def run(input, conf, filepath=None, skip_suggestions=None, fix=None):
    """Lints a YAML source.

    Returns a generator of LintProblem objects.

    :param input: buffer, string or stream to read from
    :param conf: yamllint configuration object
    :param filepath: The config file path.
    :param skip_suggestions: Do not suggest changes in lint message.
    :param autofix: fix changes in place.
    """

    if conf.is_file_ignored(filepath):
        return ()

    base_path = os.path.dirname(os.path.abspath(input.name))

    if isinstance(input, (bytes, str)):
        base_path = os.path.dirname(os.path.abspath(input.name))
        return _run(input,
                    conf,
                    filepath,
                    input_file=input.name,
                    base_path=base_path,
                    skip_suggestions=skip_suggestions,
                    fix=fix)
    elif hasattr(input, 'read'):  # Python 2's file or Python 3's io.IOBase
        # We need to have everything in memory to parse correctly
        content = input.read()
        return _run(content,
                    conf,
                    filepath,
                    input_file=input.name,
                    base_path=base_path,
                    skip_suggestions=skip_suggestions,
                    fix=fix)
    else:
        raise TypeError('input should be a string or a stream')
