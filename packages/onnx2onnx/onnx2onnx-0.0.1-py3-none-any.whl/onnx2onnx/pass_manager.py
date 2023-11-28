"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import copy
from contextlib import suppress
from typing import Callable, List

from .graph import OnnxGraph
from .passes.convert import half_to_float
from .passes.transforms import split_to_slice


class PassManager:
    """Ordered optimization pass list.

    Args:
        include (List[str], Optional): a list of pattern to select passes.
            Defaults to select all passes.
        exclude (List[str], Optional): a list of pattern to deselect passes.
            Defaults to None.
    """

    passes: List[Callable[[OnnxGraph], OnnxGraph]] = [
        half_to_float,
        split_to_slice,
    ]

    def __init__(self, include: List[str] = None, exclude: List[str] = None) -> None:
        self.activated = []
        if not include:
            self.activated = copy.deepcopy(PassManager.passes)
        else:
            self.activated = [i for i in PassManager.passes if i.__name__ in include]
        if exclude:
            self.activated = list(filter(lambda i: i not in exclude, self.activated))

    def optimize(self, graph: OnnxGraph, strict: bool = False) -> OnnxGraph:
        """Invoke passes on the input graph.

        Args:
            graph (OnnxGraph): See :class:`OnnxGraph`.
            strict (bool): Break if any pass fails.
        """
        for opt in self.activated:
            try:
                graph = opt(graph)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(f"[E] {opt.__name__} failed: {ex}")
                if strict:
                    raise
        return graph

    @classmethod
    def print_all(cls):
        """Print the name of all passes."""
        msg = "\n".join([f"{i.__name__}" for i in cls.passes])
        print(msg, flush=True)


with suppress(ImportError):
    import onnxoptimizer

    def onnx_optimizer(graph):
        """Fuse op and remove isolated nodes."""
        return OnnxGraph(onnxoptimizer.optimize(graph.model))

    PassManager.passes.append(onnx_optimizer)
