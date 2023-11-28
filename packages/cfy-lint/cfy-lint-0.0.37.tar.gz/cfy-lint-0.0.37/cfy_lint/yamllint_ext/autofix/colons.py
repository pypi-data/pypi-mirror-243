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

import re

from cfy_lint.yamllint_ext.autofix.utils import filelines, get_eol


def fix_colons(problem):
    if problem.rule == 'colons':
        with filelines(problem.file) as lines:
            line = lines[problem.line - 1]
            if re.match(r'^\s*([^:\n]+)\s*:\s*([^:\n]+)\s*$', line):
                new_line = re.sub(r'\s*:\s*', ': ', line)
            elif re.match(r'^\s*([^:\n]+)\s*:\s*$', line):
                new_line = re.sub(r'\s*:', ': ', line)
            striped_new_line, eol = get_eol(new_line)
            if new_line[-1] != eol:
                new_line = striped_new_line + eol
            lines[problem.line - 1] = new_line
        problem.fixed = True
