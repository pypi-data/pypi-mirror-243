# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console
from typer_config.decorators import dump_json_config, use_json_config

from eztransformer import setup_experiment

setup_experiment()

import torch
from eztils.typer import dataclass_option

from eztransformer import DEBUG, LOG_DIR, version
from eztransformer.gpt import GPT, GPTConfig

app = typer.Typer(
    name="eztransformer",
    help="faster, simpler, more interpretable nanoGPT",
    pretty_exceptions_enable=False,
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]eztransformer[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
@use_json_config()
@dump_json_config(str(LOG_DIR / "config.json"))
def main(
    experiment_name: str = typer.Option("debug", prompt=not DEBUG),
    gpt_config: dataclass_option(GPTConfig) = "{}",
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the eztransformer package.",
    ),
) -> None:

    gpt_config: GPTConfig = gpt_config

    model = GPT(gpt_config)
    print("Testing forward pass...")
    test_input = torch.randn((1, 2, gpt_config.n_embd))
    output = model(test_input)
    print("Passed!")


app()
