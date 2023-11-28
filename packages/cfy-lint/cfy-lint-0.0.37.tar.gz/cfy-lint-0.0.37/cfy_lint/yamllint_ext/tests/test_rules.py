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

from mock import Mock, patch
import yaml

from . import get_loader, get_gen_as_list

from .. import rules
from .. import LintProblem
from ..cloudify import models
from ..generators import (
    CfyNode,
    generate_nodes_recursively)
from ..rules.constants import (
    TFLINT_SUPPORTED_CONFIGS,
    TERRATAG_SUPPORTED_FLAGS)


def get_mock_cfy_node(content, top_level_type, curr_node_index=1):
    loaded_yaml = get_loader(content)
    loaded_yaml.check_node()
    curr_node = get_gen_as_list(
        generate_nodes_recursively, loaded_yaml.get_node().value)
    node = Mock()
    node.start_mark = Mock(line=100)
    node.end_mark = Mock(line=200)
    node.value = curr_node[curr_node_index].value
    prev = Mock(node=Mock(value=top_level_type))
    elem = CfyNode(node, prev)
    elem.line = 1
    return elem


def test_capabilities():
    capability_content = """
    capabilities:
      key_content:
        description: Private agent key
        shmalue: { get_attribute: [agent_key, private_key_export] }
    """
    elem = get_mock_cfy_node(capability_content, 'capabilities')
    result = get_gen_as_list(rules.capabilities.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "capability key_content does not provide a value" in \
           result[0].message

    output_content = """
    outputs:
      key_content:
        description: Private agent key
        shmalue: { get_attribute: [agent_key, private_key_export] }
    """
    elem = get_mock_cfy_node(output_content, 'outputs')
    result = get_gen_as_list(rules.capabilities.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "output key_content does not provide a value" in \
           result[0].message


def test_dsl_definition():
    dsl_def_content_a = """
    dsl_definitions:
      1: &foo
        foo: bar
    """
    elem = get_mock_cfy_node(dsl_def_content_a, 'dsl_definitions')
    result = get_gen_as_list(rules.dsl_definitions.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "dsl definition should be a string and " \
           "should not start with a numeric character" in result[0].message

    dsl_def_content_2 = """
    dsl_definitions:
      foo: &foo
        - foo
    """
    elem = get_mock_cfy_node(dsl_def_content_2, 'dsl_definitions')
    result = get_gen_as_list(rules.dsl_definitions.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "dsl definition foo content must be a dict" in \
           result[0].message


def test_dsl_versions():
    dsl_version_content = """
    tosca_definitions_version: cloudify_dsl_1_5
    """
    elem = get_mock_cfy_node(dsl_version_content, 'tosca_definitions_version')
    result = get_gen_as_list(rules.dsl_version.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "dsl_version not supported: cloudify_dsl_1_5" in \
           result[0].message


def test_imports():
    output_content = """
    imports:
      - ftp://cloudify.co/spec/cloudify/6.3.0/types.yaml
      - plugin:cloudify-openstack-plugin?version= <=3.0.0
    """
    elem = get_mock_cfy_node(output_content, 'imports')
    result = get_gen_as_list(rules.imports.check, {'token': elem})
    assert isinstance(result[0], LintProblem)
    assert "ftp scheme not accepted" in result[0].message
    assert isinstance(result[1], LintProblem)
    assert "Cloudify Openstack Plugin version ['version= <=3.0.0']" in \
           result[1].message


def test_inputs():
    input_content = """
    inputs:
      taco:
        description: taco
        default: 'taco'
    """
    elem = get_mock_cfy_node(input_content, 'inputs')
    result = get_gen_as_list(rules.inputs.check, {'token': elem,
                                                  'skip_suggestions': ()})
    assert isinstance(result[0], LintProblem)
    assert '"taco" does not specify a type. ' \
           'The correct type could be "string".' in result[0].message
    input_content_2 = """
    node_templates:
      foo:
        type: cloudify.nodes.Foo
        properties:
          bar: { get_input: baz }
    """

    elem = get_mock_cfy_node(input_content_2, 'get_input')
    with patch('cfy_lint.yamllint_ext.rules.inputs.ctx') as ctx:
        ctx['inputs'] = {}
        result = get_gen_as_list(rules.inputs.check, {'token': elem})
        assert isinstance(result[0], LintProblem)
        assert 'undefined input' in result[0].message


def test_node_templates():
    node_templates_content = """
    node_templates:

      foo:
        type: cloudify.azure.nodes.ResourceGroup
        properties:
          azure_config:
            foo: bar
          baz: { get_input: taco }
          quk: { get_attribute: [ quuk, quuz ] }
    """

    elem = get_mock_cfy_node(node_templates_content, 'node_templates')
    context = {
        'foo': models.NodeTemplate('foo'),
    }
    with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
        ctx['inputs'] = {}
        result = get_gen_as_list(rules.node_templates.check,
                                 {'token': elem, 'context': context})

        assert isinstance(result[0], LintProblem)
        assert 'deprecated node type' in result[0].message
        assert isinstance(result[1], LintProblem)
        assert 'undefined input' in result[1].message
        assert isinstance(result[2], LintProblem)
        assert 'undefined target' in result[2].message
        assert isinstance(result[3], LintProblem)
        assert 'deprecated property' in result[3].message


def test_node_types():
    node_types_content = """
    node_types:
      foo:
        derived_from: cloudify.nodes.Root
    """
    with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
        ctx['imported_node_types'] = {
            'foo': yaml.safe_load(
                node_types_content)['node_types']['foo']
        }
    elem = get_mock_cfy_node(node_types_content, 'node_types')
    result = get_gen_as_list(
        rules.node_types.check,
        {
            'token': elem,
            'skip_suggestions': ()
        }
    )
    assert result == []


def test_relationships():
    relationships_content = """
    node_templates:
      foo:
        type: cloudify.nodes.Foo
        relationships:
        - type: cloudify.azure.relationships.contained_in_resource_group
          target: foo
    """
    # elem = get_mock_cfy_node(relationships_content, 'relationships')
    loaded_yaml = get_loader(relationships_content)
    loaded_yaml.check_node()
    curr_node = get_gen_as_list(
        generate_nodes_recursively, loaded_yaml.get_node().value)
    prev = Mock(node=Mock(value='relationships'))
    elem = CfyNode(curr_node[7], prev)
    elem.line = 1
    elem.node_templates = ['foo', 'bar']
    result = get_gen_as_list(rules.relationships.check, {'token': elem})

    assert 'deprecated relationship type' in result[0].message


def test_tflint():
    node_templates_content = """
    node_templates:
      cloud_resources:
        type: cloudify.nodes.terraform.Module
        properties:
          tflint_config:
            config:
            - type_name: configinvalid
            - type_name: config
              option_value_invalid:
                module: 'true'
            - type_name: plugin
              option_name_invalid: aws
              option_value:
                enabled: 'false'
            flags_override:
              - loglevel: info
              - color
            enable: false
    """

    elem = get_mock_cfy_node(node_templates_content, 'node_templates')
    context = {
        'cloud_resources': models.NodeTemplate('cloud_resources'),
    }

    with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
        ctx['inputs'] = {}
        result = get_gen_as_list(
            rules.node_templates.check,
            {
                'token': elem,
                'context': context,
                'node_types': ['cloudify.nodes.terraform.Module']
            }
        )
        result.pop(0)
        assert isinstance(result[0], LintProblem)
        assert 'tflint_config will have no effect if "enable: false".' \
               in result[0].message
        assert isinstance(result[1], LintProblem)
        assert 'unsupported key {} in tflint_config.'\
            .format(TFLINT_SUPPORTED_CONFIGS) in result[1].message
        assert isinstance(result[2], LintProblem)
        assert 'To use tflint with type_name: config, it is necessary to ' \
               'write option_value' in result[2].message
        assert isinstance(result[3], LintProblem)
        assert 'tflint_config "type_name" key must also provide ' \
               '"option_name", which is the plugin name.' in result[3].message
        assert isinstance(result[4], LintProblem)
        assert 'color flag is not supported in flags_override'\
               in result[4].message


def test_tfsec():
    node_templates_content = """
    node_templates:
      cloud_resources:
        type: cloudify.nodes.terraform.Module
        properties:
          tfsec_config:
            config:
              "exclude" : 'invalid'
            flags_override: [color]
            enable: false
    """

    elem = get_mock_cfy_node(node_templates_content, 'node_templates')
    context = {
        'cloud_resources': models.NodeTemplate('cloud_resources'),
    }

    with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
        ctx['inputs'] = {}
        result = get_gen_as_list(
            rules.node_templates.check,
            {
                'token': elem,
                'context': context,
                'node_types': ['cloudify.nodes.terraform.Module']
            }
        )
        result.pop(0)
        assert isinstance(result[0], LintProblem)
        assert 'tfsec_config will have no effect if "enable: false".' \
               in result[0].message
        assert isinstance(result[1], LintProblem)
        assert 'tfsec_config.config parameters "include" and "exclude" ' \
               'should be a list' in result[1].message
        assert isinstance(result[2], LintProblem)
        assert 'Color flag cannot be used in flags_override' \
               in result[2].message


def test_terratag():
    node_templates_content = """
    node_templates:
      cloud_resources:
        type: cloudify.nodes.terraform.Module
        properties:
          terratag_config:
            tags: { 'name_company': 'cloudify' }
            flags_override:
              - -verbose: True
              - abc: 'abc'
    """

    elem = get_mock_cfy_node(node_templates_content, 'node_templates')
    context = {
        'cloud_resources': models.NodeTemplate('cloud_resources'),
    }

    with patch('cfy_lint.yamllint_ext.rules.node_templates.ctx') as ctx:
        ctx['inputs'] = {}

        result = get_gen_as_list(
            rules.node_templates.check,
            {
                'token': elem,
                'context': context,
                'node_types': ['cloudify.nodes.terraform.Module']
            }
        )
        result.pop(0)
        assert isinstance(result[0], LintProblem)
        assert 'The flags should be without a "-" sign, -verbose' \
               in result[0].message
        assert isinstance(result[1], LintProblem)
        assert "unsupported flag, ['dir', 'skipTerratagFiles', 'verbose'," \
               " 'filter']" in result[1].message
        assert isinstance(result[2], LintProblem)
        assert "unsupported flag, {}".format(TERRATAG_SUPPORTED_FLAGS) \
               in result[2].message
        assert isinstance(result[3], LintProblem)
        assert 'cloudify.nodes.terraform.Module type should ' \
               'be used with some policy validation product' \
               in result[3].message


def test_prep_cyclic():
    buffer = '''
node_templates:

  d1:
    type: cloudify.nodes.gcp.Volume
    properties:
      client_config: gcp_config
      image: { get_input: image }
      size: 20
      boot: true
    relationships:
      - type: cloudify.relationships.connected_to
        target: d2
  d2:
    type: cloudify.nodes.gcp.Volume
    properties:
      client_config: gcp_config
      image: { get_input: image }
      size: 20
      boot: true
    relationships:
      - type: cloudify.relationships.connected_to
        target: d3
  d3:
    type: cloudify.nodes.gcp.Volume
    properties:
      client_config: gcp_config
      image: { get_input: image }
      size: 20
      boot: true
    relationships:
      - type: cloudify.relationships.connected_to
        target: d1

  d4:
    type: cloudify.nodes.gcp.Volume
    properties:
      gcp_config: gcp_config
      image: { get_input: image }
      size: 20
      boot: true
    relationships:
      - type: cloudify.relationships.connected_to
        target: d5

  d5:
    type: cloudify.nodes.gcp.Volume
    properties:
      client_config: gcp_config
      image: { get_input: image }
      size: 20
      boot: true
    relationships:
      - type: cloudify.relationships.connected_to
        target: d4

    '''
    edges = []
    line_index = {}
    expected_edges = [('d1', 'd2'), ('d2', 'd3'), ('d3', 'd1'),
                      ('d4', 'd5'), ('d5', 'd4')]
    expected_line_index = {'d1': 0, 'd2': 1, 'd3': 2, 'd4': 3, 'd5': 4}
    line = 0
    inputs = list(node_generator(buffer))
    for input in inputs[1].value:
        edges, line_index = rules.node_templates.prepre_cyclic_inputs(
          input, edges, line_index, line
        )
        line = line + 1
    assert edges == expected_edges
    assert line_index == expected_line_index


def node_generator(buffer):
    yaml_loader = SafeLineLoader(buffer)
    if not yaml_loader.check_node():
        return
    yield from generate_nodes_recursively(yaml_loader.get_node().value)


class SafeLineLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(
            node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping


def test_cyclic():
    edges = [('n1', 'n2'),
             ('n2', 'n3'),
             ('n3', 'n1'),
             ('n4', 'n5'),
             ('n5', 'n4')]
    lines_index = {
        'n1': 47, 'n2': 57, 'n3': 67, 'n4': 78, 'n5': 89}
    results = rules.node_templates.check_cyclic_node_dependency(
        edges, lines_index)
    expected_results_message = [
        "A dependency loop consistent of ['n4', 'n5'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n5', 'n4'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n1', 'n2', 'n3'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n1', 'n3', 'n2'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n2', 'n1', 'n3'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n2', 'n3', 'n1'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n3', 'n2', 'n1'] "
        "was identified (auto-fix unavailable)",
        "A dependency loop consistent of ['n3', 'n1', 'n2'] "
        "was identified (auto-fix unavailable)"
    ]
    for result in results:
        assert result.message in expected_results_message
