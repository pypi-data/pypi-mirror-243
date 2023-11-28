"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import numpy as np
from onnx import NodeProto, numpy_helper
from onnx.helper import make_node


def make_constant(name: str, value: np.ndarray) -> "NodeProto":
    """Make a Constant node according to given value."""
    node = make_node(
        op_type="Constant",
        name=name,
        inputs=[],
        outputs=[f"{name}_output_0"],
        value=numpy_helper.from_array(value),
    )
    return node
