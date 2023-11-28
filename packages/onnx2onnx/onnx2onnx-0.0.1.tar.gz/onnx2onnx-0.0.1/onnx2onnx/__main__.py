"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""
# pylint: disable=missing-function-docstring
import argparse
from pathlib import Path

import onnx
from onnx import _DEFAULT_FORMAT as ONNX_DEFAULT_FORMAT

from .graph import OnnxGraph
from .pass_manager import PassManager

USAGE = "onnx2onnx input_model.onnx [output_model.onnx]"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="onnx2onnx",
        usage=USAGE,
        description="onnx2onnx command-line api",
    )
    parser.add_argument(
        "-a",
        "--activate",
        nargs="*",
        help="select passes to be activated, activate all passes if not set.",
    )
    parser.add_argument(
        "-d",
        "--deactivate",
        nargs="*",
        help="deselect activated passes, exclusive to '--activate'",
    )
    parser.add_argument(
        "--print-all",
        action="store_true",
        help="print the name of all optimizing passes",
    )
    parser.add_argument(
        "--format",
        choices=("protobuf", "textproto", "json", "onnxtxt"),
        default=ONNX_DEFAULT_FORMAT,
        help="onnx file format",
    )

    return parser.parse_known_args()


def main():
    args, argv = parse_args()

    if args.print_all:
        PassManager.print_all()
        exit(0)
    if args.activate and args.deactivate:
        raise RuntimeError("--activate and --deactivate are exclusive!")
    if len(argv) == 1:
        input_model = Path(argv[0])
        output_model = Path(input_model.stem + "_o2o")
    elif len(argv) == 2:
        input_model = Path(argv[0])
        output_model = Path(argv[1])
    else:
        print("Usage: " + USAGE)
        if len(argv) == 0:
            raise RuntimeError("missing input model")
        else:
            raise RuntimeError("unknown argument: " + ",".join(argv[2:]))

    pm = PassManager(include=args.activate, exclude=args.deactivate)
    graph = OnnxGraph(onnx.load_model(input_model, format=args.format))
    graph = pm.optimize(graph, strict=False)
    graph.save(output_model, format=args.format)
    print(f"model saved to {output_model}")


if __name__ == "__main__":
    main()
