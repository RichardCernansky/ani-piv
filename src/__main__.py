"""Command-line entry point for the PIV project.

Run from the project/ folder:
    python -m src show  [-c CONFIG]
    python -m src build [-c CONFIG] 
    python -m src train [-c CONFIG] [--epochs N]
    python -m src test  [-c CONFIG][--checkpoint PATH]

The config is a Python file (e.g. src/configs/config.py). Command-line
options override values from it.
"""
import argparse
import importlib.util
from pathlib import Path


def load_config(path):
    """Load a .py config file as a module object (cfg.viz, cfg.cilia, ...)."""
    path = Path(path)
    if not path.is_file():
        raise SystemExit(f"config not found: {path.resolve()}")
    spec = importlib.util.spec_from_file_location("piv_config", path)
    # create empty module object
    cfg = importlib.util.module_from_spec(spec)
    # executet the module in its own namespace
    spec.loader.exec_module(cfg)
    # save path for reference
    cfg.path = str(path)
    return cfg


# -COMMMANDS-
def cmd_show(cfg, args):
    from viz.show import main
    main(cfg)


def cmd_build(cfg, args):
    from src.pipeline.build_dataset import main
    main(cfg)


# def cmd_train(cfg, args):
#     if args.epochs:
#         cfg.train["epochs"] = args.epochs

#     from src.model.train import main
#     main(cfg)


# def cmd_test(cfg, args):
#     if args.checkpoint:
#         cfg.test["checkpoint"] = args.checkpoint

#     from src.model.evaluate import main
#     main(cfg)


#parser
def build_parser():
    # shared by every subcommand, so -c goes after the command name
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-c", "--config", default="src/configs/config.py",
                    help="path to config .py file (default: %(default)s)")

    parser = argparse.ArgumentParser(prog="piv", description="PCD cilia pipeline")
    #args.command  registers "build"
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("show", parents=[common], help="visualise enhancement / Otsu steps")
    # register cmd_show() as the function to call when this subcommand is used
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("build", parents=[common], help="build the cilia patch dataset")
    # register cmd_build() as the function to call when this subcommand is used
    p.set_defaults(func=cmd_build)

    # p = sub.add_parser("train", parents=[common], help="train the U-Net")
    # p.add_argument("--epochs", type=int)
    # p.set_defaults(func=cmd_train)

    # p = sub.add_parser("test", parents=[common], help="evaluate a trained model")
    # p.add_argument("--checkpoint", help="path to model weights")
    # p.set_defaults(func=cmd_test)

    return parser


def main():
    # parse command-line args and load config
    args = build_parser().parse_args()
    cfg = load_config(args.config)
    print(f"[{args.command}] config: {cfg.path}")

    # call the function registered for this subcommand
    args.func(cfg, args)


if __name__ == "__main__":
    main()