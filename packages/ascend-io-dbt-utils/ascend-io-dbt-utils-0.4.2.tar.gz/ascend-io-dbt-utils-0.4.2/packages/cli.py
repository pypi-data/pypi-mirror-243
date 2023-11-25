import click
import json

from dotenv import load_dotenv

from packages import process_module
from packages import run_tests_module

# Silently try to load the .env file if it exists
load_dotenv()

@click.group(
        help="""
        Collection of utilities to help convert dbt projects into Ascend dataflows.
        """)
def cli():
    pass

def ascend_options(f):
    f = click.option('--hostname', required=True, help='Ascend hostname. envvar=ASCEND_HOSTNAME', envvar='ASCEND_HOSTNAME')(f)
    f = click.option('--data-service', required=True, help='Ascend data service name, envvar=ASCEND_DATA_SERVICE', envvar='ASCEND_DATA_SERVICE')(f)
    f = click.option('--dataflow', required=True, help='Ascend dataflow name, envvar=ASCEND_DATAFLOW', envvar='ASCEND_DATAFLOW')(f)
    return f

def load_json(ctx, param, value):
    """
    Callback to load the JSON file into the context object when --manifest-file is passed.
    """
    if not value or ctx.resilient_parsing:
        return
    try:
        with open(value, 'r') as f:
            manifest = json.load(f)
        ctx.ensure_object(dict)
        ctx.obj['manifest'] = manifest
    except Exception as e:
        raise click.BadParameter(f"Could not load JSON file: {e}")
    return value

def manifest_options(f):
    f = click.option('--manifest-file', required=True, help='Path to the manifest JSON file, envvar=DBT_MANIFEST_FILE', envvar='DBT_MANIFEST_FILE', type=click.Path(exists=True), callback=load_json)(f)
    return f


@click.command()
@click.pass_context
@ascend_options
@manifest_options
@click.option('--default-seed', required=False, help='Default seed to connect hanging models to. Defaults to one of the nodes in the dataflow, envvar=DEFAULT_SEED', envvar='DEFAULT_SEED')
def merge(ctx, **kwargs):
    """Process the compiled dbt manifest and SQL files and create/update/delete Ascend dataflow transforms."""
    process_module.merge_cmd(ctx, **kwargs)
cli.add_command(merge)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def update_sql(ctx, **kwargs):
    """Update the SQL of existing Ascend dataflow transforms."""
    process_module.update_sql_cmd(ctx, **kwargs)
cli.add_command(update_sql)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def delete(ctx, **kwargs):
    """Delete all dbt models from an Ascend dataflow."""
    process_module.delete_cmd(ctx, **kwargs)
cli.add_command(delete)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def validate(ctx, **kwargs):
    """Validate the seeds and sources are present in the dataflow."""
    process_module.validate_cmd(ctx, **kwargs)
cli.add_command(validate)

@click.command()
@click.pass_context
@manifest_options
def show(ctx, **kwargs):
    """Show the dependencies of dbt models."""
    process_module.show_cmd(ctx, **kwargs)
cli.add_command(show)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
@click.option('--model-name', required=True, help='Name of the dbt model to create.')
@click.option('--reduction', required=False, help='Partition reduction to use for the component. Defaults to "no-reduction.', default='no-reduction', type=click.Choice(['no-reduction', 'full-reduction']))
@click.option('--with-tests', required=False, help='Create tests for the component.', default=False, is_flag=True)
def create_component(ctx, **kwargs):
    """Create a component from a dbt model."""
    process_module.create_component_cmd(ctx, **kwargs)
cli.add_command(create_component)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def deploy_tests(ctx, **kwargs):
    """Create and run all dbt tests against the deployed models in Ascend."""
    run_tests_module.deploy_tests_cmd(ctx, **kwargs)
cli.add_command(deploy_tests)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def delete_tests(ctx, **kwargs):
    """Delete all dbt tests against the deployed models in Ascend."""
    run_tests_module.delete_tests_cmd(ctx, **kwargs)
cli.add_command(delete_tests)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def check_test_results(ctx, **kwargs):
    """Check the results of all dbt tests against the deployed models in Ascend."""
    run_tests_module.check_test_results_cmd(ctx, **kwargs)
cli.add_command(check_test_results)


if __name__ == "__main__":
    cli(prog_name='ascend_dbt_transform')