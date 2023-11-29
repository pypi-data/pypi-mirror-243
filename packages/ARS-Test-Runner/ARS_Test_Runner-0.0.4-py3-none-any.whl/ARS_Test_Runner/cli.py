# -*- coding: utf-8 -*-

import click
import ast
import os
import sys
import datetime
from copy import deepcopy
from ARS_Test_Runner.semantic_test import run_semantic_test
from pkg_resources import get_distribution, DistributionNotFound
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

try:
    __version__ = get_distribution("ARS_Test_Runner").version
except DistributionNotFound:
     # package is not installed
    pass

class PythonLiteralOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=__version__)
@click.option('--env', type=click.Choice(['dev', 'ci', 'test', 'prod'], case_sensitive=False))
@click.option('--query_type', type=click.STRING, help='default: treats_cretive', default='treats_creative')
@click.option('--expected_output', cls=PythonLiteralOption, type=click.Choice(['TopAnswer', 'Acceptable', 'BadButForgivable', 'NeverShow'], case_sensitive=False))
@click.option('--input_curie', type=click.STRING, help='Input Curie')
@click.option('--output_curie', cls=PythonLiteralOption, help='Output Curie (can be a list)')

def main(env, query_type, input_curie, output_curie, expected_output):

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S')

    click.echo(f"started performing Single Level ARS_Test Analysis at {formatted_time}")
    #pylint: disable=too-many-arguments
    pipeline = run_semantic_test(env, query_type, expected_output, input_curie, output_curie)
    endtime = datetime.datetime.now()
    click.echo(f"finished running the pipeline at {endtime}")
    return pipeline
