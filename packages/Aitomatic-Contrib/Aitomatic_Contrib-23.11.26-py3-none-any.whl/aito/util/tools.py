"""H1st CLI."""


import click

from aito.pmfp.tools import aito_pmfp_cli


@click.group(name='h1st',
             cls=click.Group,
             commands={
                 'pmfp': aito_pmfp_cli,
             },

             # Command kwargs
             context_settings=None,
             # callback=None,
             # params=None,
             help='H1st CLI >>>',
             epilog='^^^ H1st CLI',
             short_help='H1st CLI',
             options_metavar='[OPTIONS]',
             add_help_option=True,
             no_args_is_help=True,
             hidden=False,
             deprecated=False,

             # Group/MultiCommand kwargs
             invoke_without_command=False,
             subcommand_metavar='H1ST_SUB_COMMAND',
             chain=False,
             result_callback=None)
def aito_cli():
    """Aito CLI."""
