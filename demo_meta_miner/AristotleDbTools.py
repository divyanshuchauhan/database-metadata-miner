import click
import os
from demo_meta_miner.utils import get_miner_class

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class AristotleDbTools(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and not filename.startswith("_"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        # ns = {}
        # fn = os.path.join(plugin_folder, name + '.py')
        # print(fn)
        # with open(fn) as f:
        #     code = compile(f.read(), fn, 'exec')
        #     eval(code, ns, ns)
        # print(ns)
        # return ns['demo']
        klass = get_miner_class(name)
        return klass

# cli = AristotleDbTools(help='This tool\'s subcommands are loaded from a '
            # 'plugin folder dynamically.')

@click.command(cls=AristotleDbTools)
def cli():
    """
    This tool\'s subcommands are loaded from a plugin folder dynamically.
    """
    pass

if __name__ == '__main__':
    cli()