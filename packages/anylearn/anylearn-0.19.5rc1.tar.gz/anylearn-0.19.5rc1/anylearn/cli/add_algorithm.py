import click

from anylearn.cli.anylearn_cli_config import AnylearnCliConfig
from anylearn.cli.utils import (
    check_config,
    check_connection,
    cmd_error,
    cmd_success,
    get_cmd_command,
)
from anylearn.interfaces import Algorithm


@click.group("algorithm")
@check_config()
def commands():
    """
    Add local or remote algorithm to local Anylearn project.
    """
    pass


@commands.command()
@get_cmd_command()
@click.argument('name')
@click.option(
    '-d', '--dir',
    prompt=True,
    help="Local algorithm folder (absolute path)."
)
@click.option(
    '-i', '--image',
    default='QUICKSTART',
    help="Container image name.",
)
def local(
    name: str,
    dir: str,
    image: str='QUICKSTART',
):
    """
    Add local algorithm to current project.
    """
    algo = Algorithm(
        name=name,
        train_params = "[]",
        follows_anylearn_norm=False,
    )
    config = AnylearnCliConfig.load()
    old_algo = config.algorithms.get(name, None)
    old_dir = config.path['algorithm'].get(name, None)
    if old_algo:
        cmd_error(msg=(
            "An algorithm with same name "
            "has already been added to current project"
            "\n(\n"
            f"  ID={old_algo.id},\n"
            f"  NAME={old_algo.name},\n"
            f"  LOCAL_DIR={old_dir},\n"
            "\n)\n"
        ))
        raise click.Abort
    config.algorithms[name] = algo
    config.path['algorithm'][name] = dir
    config.images[name] = image
    AnylearnCliConfig.update(config)
    cmd_success(msg="ADDED")


@commands.command()
@click.argument('id')
@check_connection()
@get_cmd_command()
def remote(id: str):
    """
    Add remote algorithm by ID to current project.
    """
    config = AnylearnCliConfig.load()
    try:
        old_algo = next(
            a
            for a in config.algorithms.values()
            if a.id == id
        )
        cmd_error(msg=(
            f"Remote algorithm (ID={id}, name={old_algo.name}) "
            "has already been added to current project.\n"
            "Aborted!"
        ))
    except:
        try:
            algo = Algorithm(id=id, load_detail=True)
            config = AnylearnCliConfig.load()
            old_algo = config.algorithms.get(algo.name, None) # type: ignore
            old_dir = config.path['algorithm'].get(algo.name, None) # type: ignore
            if old_algo:
                cmd_error(msg=(
                    "An algorithm with same name "
                    "has already been added to current project"
                    "\n(\n"
                    f"  ID={old_algo.id},\n"
                    f"  NAME={old_algo.name},\n"
                    f"  LOCAL_DIR={old_dir},\n"
                    "\n)\n"
                ))
                raise click.Abort
            config.algorithms[algo.name] = algo # type: ignore
            config.path['algorithm'][algo.name] = None # type: ignore
            AnylearnCliConfig.update(config)
            cmd_success(msg="ADDED")
        except:
            cmd_error(msg=(
                f"Remote algorithm (ID={id}) does not exist.\n"
                "Aborted!"
            ))
