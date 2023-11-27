import unittest
import os

from packages.manifest_utils import _get_nodes_and_dependencies

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", 'python')

class TestParseManifest(unittest.TestCase):
    def test_parse_manifest(self):
        manifest = {
            'sources': {
                'source1': {},
                'source2': {}
            },
            'nodes': {
                'node1': {
                    'resource_type': 'model',
                    'depends_on': {
                        'nodes': ['source1', 'source2']
                    }
                },
                'node2': {
                    'resource_type': 'seed',
                    'depends_on': {
                        'nodes': ['node1']
                    }
                }
            }
        }
        expected_nodes = ['source1', 'source2', 'node1', 'node2']
        expected_dependencies = {
            'node1': ['source1', 'source2'],
            'node2': ['node1'],
            'source1': [],
            'source2': []
        }
        nodes, dependencies = _get_nodes_and_dependencies(manifest)

        self.assertListEqual(nodes, expected_nodes)
        self.assertDictEqual(dependencies, expected_dependencies)

    def test_parse_manifest_with_default_seed(self):
        manifest = {
            'sources': {
                'source1': {},
                'source2': {}
            },
            'nodes': {
                'model1': {
                    'resource_type': 'model',
                    'depends_on': {
                        'nodes': ['source1', 'source2']
                    }
                },
                'model2': {
                    'resource_type': 'model',
                    'depends_on': {
                        'nodes': ['model1']
                    }
                },
                'seed1': {
                    'resource_type': 'seed',
                    'depends_on': {
                        'nodes': ['model2']
                    }
                }
            }
        }
        default_seed = 'default_seed'
        expected_dependencies = {
            'model1': ['source1', 'source2'],
            'model2': ['model1'],
            'seed1': ['model2'],
            'source1': [],
            'source2': [],
        }
        nodes, dependencies = _get_nodes_and_dependencies(manifest, default_seed)
        self.assertDictEqual(dependencies, expected_dependencies)

if __name__ == '__main__':
    unittest.main()