import sys
import click
from ordo import __version__

class OrdoGroup(click.Group):
    def parse_args(self, ctx, args):
        # If first arg looks like group:command, handle it directly
        if args and ":" in args[0]:
            ctx.obj = {"command": args[0], "config_path": None}
            for i, arg in enumerate(args):
                if arg == "--config" and i + 1 < len(args):
                    ctx.obj["config_path"] = args[i + 1]
            return []
        return super().parse_args(ctx, args)

    def invoke(self, ctx):
        if ctx.obj and "command" in ctx.obj:
            from ordo.config import load_config
            from ordo.runner import Runner
            try:
                config = load_config(ctx.obj["config_path"])
                code = Runner.execute(config, ctx.obj["command"])
                sys.exit(code)
            except Exception as e:
                click.echo(f"✗ {e}", err=True)
                sys.exit(1)
        else:
            super().invoke(ctx)

@click.group(cls=OrdoGroup, invoke_without_command=True)
@click.version_option(__version__, prog_name="ordo")
@click.pass_context
def main(ctx):
    """Ordo — structured command runner."""
    if ctx.invoked_subcommand is None and (ctx.obj is None or "command" not in ctx.obj):
        click.echo(ctx.get_help())

@main.command("list")
@click.option("--verbose", "-v", is_flag=True, help="Show raw run strings.")
@click.option("--config", "config_path", default=None, help="Path to ordo.yaml.")
def list_cmd(verbose, config_path):
    """List all available commands."""
    from ordo.config import load_config
    from ordo.lister import Lister
    try:
        config = load_config(config_path)
        Lister.list(config, verbose=verbose)
    except Exception as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)

@main.command("validate")
@click.option("--config", "config_path", default=None, help="Path to ordo.yaml.")
def validate_cmd(config_path):
    """Validate ordo.yaml before runtime."""
    from ordo.config import load_config
    from ordo.validator import Validator
    try:
        config = load_config(config_path)
        errors = Validator.validate(config)
        if errors:
            click.echo(f"✗ ordo.yaml has {len(errors)} error(s):\n", err=True)
            for e in errors:
                click.echo(f"  {e}", err=True)
            sys.exit(1)
        total_commands = sum(len(g.commands) for g in config.groups.values())
        click.echo(f"✓ ordo.yaml is valid ({len(config.groups)} groups, {total_commands} commands)")
    except Exception as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)