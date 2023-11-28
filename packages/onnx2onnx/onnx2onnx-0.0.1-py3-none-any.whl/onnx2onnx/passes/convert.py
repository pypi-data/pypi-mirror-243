"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import itertools

from onnx import TensorProto
from onnx.helper import make_attribute
from onnx.numpy_helper import from_array, to_array

from onnx2onnx.graph import OnnxGraph

from .utils import make_constant


def half_to_float(graph: OnnxGraph) -> OnnxGraph:
    """Convert half consts and values to float32."""

    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        if node_pb.op_type == "Constant":
            tensor = node_pb.attribute[0].t
            if tensor.data_type == TensorProto.FLOAT16:
                array = to_array(tensor).astype("float32")
                attr = make_attribute(key="value", value=from_array(array))
                node_pb.attribute.pop()
                node_pb.attribute.append(attr)
    for init in graph.initializer:
        if init.data_type == TensorProto.FLOAT16:
            array = to_array(init).astype("float32")
            init.data_type = TensorProto.FLOAT
            init.raw_data = from_array(array).raw_data
    for io in itertools.chain(graph.input, graph.output):
        if io.type.tensor_type.elem_type == TensorProto.FLOAT16:
            io.type.tensor_type.elem_type = TensorProto.FLOAT
    return graph


def initializer_to_constant(graph: OnnxGraph) -> OnnxGraph:
    """Convert initializer value to node Constant."""
    node_to_add = []
    init_names = []
    for init in graph.initializer:
        init_names.append(init.name)
        node_to_add.append(make_constant(init.name, to_array(init)))
    while graph.initializer:
        graph.initializer.pop()
    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        for i, name in enumerate(node_pb.input):
            if name in init_names:
                node_pb.input[i] = name + "_output_0"
    for node in node_to_add:
        graph.add_onnx_node(node)
    return graph
