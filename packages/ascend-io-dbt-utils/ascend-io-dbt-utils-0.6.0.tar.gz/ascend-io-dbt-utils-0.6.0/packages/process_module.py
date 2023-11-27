from ascend.sdk import definitions
from ascend.sdk.applier import DataflowApplier
from ascend.sdk.client import Client

from .manifest_utils import _get_nodes_and_dependencies
from .transform_utils import _create_transform, _translate_sql
from .run_tests_module import _get_tests_and_nodes


# This is currently only handling models, sources and seeds
def show_cmd(ctx, **kwargs):
    """
    Load and parse manifest JSON file and print the dependencies of dbt models.
    """

    nodes, dependencies = _get_nodes_and_dependencies(ctx.obj['manifest'])

    # Print nodes in topological order
    for node in nodes:
        print(f"\nNode: {node}. Depends on:")
        for dependency in dependencies[node]:
            print(f"  -> {dependency}")

def merge_cmd(ctx, **kwargs):
    """
    Merge dbt models into an Ascend dataflow.
    """
    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    # Get existing nodes in dataflow
    existing_nodes = client.list_dataflow_components(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], deep=True).data
    existing_node_ids = [node.id for node in existing_nodes]

    manifest = ctx.obj['manifest']
    nodes, dependencies = _get_nodes_and_dependencies(manifest=manifest, default_seed=existing_node_ids[0] if ctx.params['default_seed'] is None else ctx.params['default_seed'])

    # Ensure seed nodes present in the manifest are present in the dataflow. Exit if not.
    for node_str in nodes:
        if hasattr(manifest['nodes'], node_str) and manifest['nodes'][node_str]['resource_type'] in ['seed', 'source']:
            node = node_str.split('.')[-1]
            if node not in existing_node_ids:
                print(f"Seed node {node} is not present in the dataflow. Please add it manually and try again.")
                exit(1)

    # For every "model" node create a component
    components = []
    for node_str in nodes:

        # Skip if node is not a model
        if node_str.split('.')[0] != 'model':
            continue

        node = node_str.split('.')[-1]
        # Create component
        component = _create_transform(
            id=node, 
            sql=_get_compiled_sql(manifest=manifest, node_str=node_str), 
            inputs=dependencies[node_str],
            description=_get_description(manifest=manifest, node_str=node_str)
        )
        # Add component to list of existing nodes
        components.append(component)

    # Get dataflow definition
    dataflow_def = client.get_dataflow(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow']).data

    # Perform a non-deleting append
    applier = DataflowApplier(client)
    applier.apply(data_service_id=ctx.params['data_service'], dataflow=definitions.Dataflow(id=dataflow_def.id, name=dataflow_def.name, components=components), delete=False, dry_run=False)

def delete_cmd(ctx, **kwargs):
    """
    Delete dbt models from Ascend dataflow.
    """
    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    nodes, _ = _get_nodes_and_dependencies(manifest=ctx.obj['manifest'])

    # Remove all nodes from the list of existing nodes in reverse order
    node_ids = [node.split('.')[-1] for node in reversed(nodes) if node.split('.')[0] == 'model']
    for node in node_ids:
        print(f"Deleting transform {node}")
        try:
            client.delete_transform(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], id=node)
        except Exception as e:
            print(f"Could not delete transform {node}. Error: {e.reason}")

def validate_cmd(ctx, **kwargs):
    """
    Validate the seeds are present in the dataflow.
    """
    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    nodes, _ = _get_nodes_and_dependencies(manifest=ctx.obj['manifest'])

    # Validate the seeds are present in the dataflow
    node_ids = [node.split('.')[-1] for node in nodes if node.split('.')[0] in ['seed', 'source']]

    # Get existing nodes in dataflow
    existing_nodes = client.list_dataflow_components(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], deep=True).data
    existing_node_ids = [node.id for node in existing_nodes]

    # Print the list of nodes present and absent in the dataflow
    print("Nodes present in the dataflow:")
    for node in node_ids:
        if node in existing_node_ids:
            print(f"  {node}")
    print("Nodes absent in the dataflow:")
    for node in node_ids:
        if node not in existing_node_ids:
            print(f"  {node}")


def update_sql_cmd(ctx, **kwargs):
    """
    Update the SQL of existing Ascend dataflow transforms.
    """

    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    nodes, dependencies = _get_nodes_and_dependencies(manifest=ctx.obj['manifest'])

    # For every node, if there is a transform with the same name, update the SQL. Otherwise, display a message.
    for node_str in nodes:
        node_type = node_str.split('.')[0]

        if node_type != 'model':
            continue

        node = node_str.split('.')[-1]
        input_ids = [node.split('.')[-1] for node in dependencies[node_str]]
        print(f"Updating SQL of the transform {node}")
        try:
            transform_body = client.get_transform(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], id=node).data
            transform_body.view.operator.spark_function.executable.code.source.inline = _translate_sql(_get_compiled_sql(manifest=ctx.obj['manifest'], node_str=node_str), input_ids)
            client.update_transform(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], transform_id=node, body=transform_body)
        except Exception as e:
            print(f"Could not update transform {node}. Error: {e.reason}") 

def update_component_sql_cmd(ctx, **kwargs):
    """
    Update the SQL of existing Ascend dataflow transform.
    """
    node = ctx.params['model_name']
    print(f"Updating SQL of the transform {node}")

    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    nodes, dependencies = _get_nodes_and_dependencies(manifest=ctx.obj['manifest'])

    node_str = [node_str for node_str in nodes if node_str.split('.')[-1] == node][0]

    input_ids = [node.split('.')[-1] for node in dependencies[node_str]]

    try:
        transform_body = client.get_transform(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], id=node).data
        transform_body.view.operator.spark_function.executable.code.source.inline = _translate_sql(_get_compiled_sql(manifest=ctx.obj['manifest'], node_str=node_str), input_ids)
        client.update_transform(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], transform_id=node, body=transform_body)
    except Exception as e:
        print(f"Could not update transform {node}. Error: {e.reason}")     


def create_component_cmd(ctx, **kwargs):
    """
    Create a component from a dbt model.
    """
    # Create Ascend Client
    client = Client(ctx.params['hostname'])

    # Get manifest nodes and their dependencies
    nodes, dependencies = _get_nodes_and_dependencies(manifest=ctx.obj['manifest'])

    # Get the list of existing dataflow components
    existing_nodes = client.list_dataflow_components(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow'], deep=True).data

    # Check that the component has all its dependencies in the dataflow
    node_id = [ key for key in nodes if key.split('.')[-1] == ctx.params['model_name'] ][0]
    for node_str in dependencies[node_id]:
        node = node_str.split('.')[-1]
        if  node not in [node.id for node in existing_nodes]:
            print(f"Node {node} is not present in the dataflow. Please add it and try again.")
            exit(1)

    # Create the component
    component = _create_transform(
        id=ctx.params['model_name'], 
        sql=_get_compiled_sql(manifest=ctx.obj['manifest'], node_str=node_id), 
        inputs=[node.split('.')[-1] for node in dependencies[node_id]],
        description=_get_description(manifest=ctx.obj['manifest'], node_str=node_id),
        reduction=ctx.params['reduction']
    )
    components = [component]

    # Deploy tests if requested
    groups = []
    if ctx.params['with_tests']:

        # Get test data
        test_data, nodes_with_test_data = _get_tests_and_nodes(ctx.obj['manifest'])

        # Get tests for the created node
        test_id = [test for test in nodes_with_test_data if test.split('.')[-1] == ctx.params['model_name']][0]
        tests = nodes_with_test_data[test_id] 

        # Create transforms for the tests
        for test_id in tests:
            test = test_data[test_id]

            # If one of the inputs is not there, don't deploy the test and report it
            test_dependencies = test['depends_on']['nodes']
            existing_components_plus_transform = {node.id for node in existing_nodes}
            existing_components_plus_transform.add(ctx.params['model_name'])
            missing_nodes = {dep.split('.')[-1] for dep in test_dependencies} - existing_components_plus_transform
            if len(missing_nodes) > 0:
                print(f"Test {test['name']} is missing the following dependencies: {missing_nodes}. Skipping test.")
                continue

            components.append(
                _create_transform(
                    id=test['name'], 
                    sql=test['compiled_code'], 
                    inputs=test['depends_on']['nodes'],
                    description=test.get('description', ''),
                    custom_dq_test_sql='select * from {{target}} WHERE 1=1',
                    reduction='full-reduction'
                )
            )

        groups = [definitions.ComponentGroup(
            id=f'{ctx.params["model_name"]}_dbt_tests',
            name=f'{ctx.params["model_name"]}_dbt_tests',
            component_ids = [transform.id for transform in components if transform.id != ctx.params['model_name']],
            description=f'{ctx.params["model_name"]} dbt tests'
            )]

    # Get dataflow definition
    dataflow_def = client.get_dataflow(data_service_id=ctx.params['data_service'], dataflow_id=ctx.params['dataflow']).data

    # Perform a non-deleting append
    applier = DataflowApplier(client)
    applier.apply(data_service_id=ctx.params['data_service'], dataflow=definitions.Dataflow(id=dataflow_def.id, name=dataflow_def.name, components=components, groups=groups), delete=False, dry_run=False)


def _get_compiled_sql(manifest, node_str):
    """
    Get compiled SQL from manifest.
    """
    return manifest['nodes'][node_str]['compiled_code']

def _get_description(manifest, node_str):
    """
    Get description from manifest.
    """
    return manifest['nodes'][node_str].get('description', '')
