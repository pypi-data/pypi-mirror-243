import ascend.protos.component.component_pb2 as component
import ascend.protos.function.function_pb2 as function
import ascend.protos.io.io_pb2 as io
import ascend.protos.operator.operator_pb2 as operator

from ascend.sdk import definitions

import re

def _create_transform(id, sql, inputs, description, custom_dq_test_sql=None, reduction='no-reduction'):
    """
    Create Ascend transform component from dbt model.
    """
    input_ids = [x.split('.')[-1] for x in inputs]

    # In sql, find all the occurrences of the input nodes with DB name and schema name using regex as per the following example
    # Example input: select * from XXX.YYY.customer_revenue_by_month
    # Example output: select * from {{ customer_revenue_by_month }}
    prev_sql = sql
    sql = _translate_sql(sql, input_ids)

    # If no substitutions were made, display the error and exit
    # Ascend does not allow a transform to have no inputs
    if sql == prev_sql:
        print(f"No inputs replaced in the file {id}.sql. Please check the file and try again.")
        exit(1)
    
    # Create transform component
    # TODO: Add support for other SQL flavours
    # TODO: Add support for other partition reduction options
    return definitions.Transform(
        id=id,
        name=id,
        description=description,
        input_ids=input_ids,
        operator=operator.Operator(
        spark_function=operator.Spark.Function(
            executable=io.Executable(
            code=io.Code(
                language=function.Code.Language(
                snowflake_sql=function.Code.Language.SnowflakeSql(
                ),
                ),
                source=io.Code.Source(
                inline=sql,
                ),
            ),
            ),
            reduction=_get_reduction(reduction_method=reduction),
            tests=_define_quality_tests(custom_dq_test_sql),
        ),
        ),
        assigned_priority=component.Priority(
        ),
    )

def _get_reduction(reduction_method):
    """
    Get the reduction method for the transform component.
    """

    if reduction_method == 'no-reduction':
        return operator.Reduction(
                    no_reduction=operator.Reduction.NoReduction(),
                )
    elif reduction_method == 'full-reduction':
        return operator.Reduction(
                    full=operator.Reduction.Full()
                )
    else:
        raise Exception(f"Reduction method {reduction_method} not supported.")


def _translate_sql(sql, input_ids):
    """
    Translate the SQL to replace the input nodes with Ascend placeholders.
    """
    for input in input_ids:
        sql = re.sub(r'\w+\.\w+\.(\w+)'.format(input), r'{{\1}}', sql)

    return sql.strip()

# TODO: Add support for standard checks
def _define_quality_tests(custom_dq_test_sql):
    """
    Define quality tests for a transform component. Only supports no checks and custom checks.
    """

    if custom_dq_test_sql is None:
        return function.QualityTests()
    
    return function.QualityTests(
            custom=[function.QualityTests.CustomCheck(
                sql=custom_dq_test_sql.strip(),
                )]
        )