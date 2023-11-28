"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""
import numpy as np
from onnx.helper import make_node

from onnx2onnx.graph import OnnxGraph

from .utils import make_constant


def split_to_slice(graph: OnnxGraph) -> OnnxGraph:
    """Change Split node to Slice node."""
    node_to_add = []
    node_to_remove = []
    for node in graph:
        node_pb = graph.nodes[node]["pb"]
        if node_pb.op_type == "Split":
            if constants := graph.constants(node_pb):
                split = constants[0]
            axis = node_pb.attribute[0].i
            starts = 0
            for i, (ch, _) in enumerate(zip(split, graph.onnx_successors(node_pb))):
                starts_node = make_constant(
                    name=f"{node}/Starts{i}", value=np.array([starts], dtype="int64")
                )
                ends_node = make_constant(
                    name=f"{node}/Ends{i}", value=np.array([starts + ch], dtype="int64")
                )
                axes_node = make_constant(
                    name=f"{node}/Axes{i}", value=np.array([axis], dtype="int64")
                )
                slice_node = make_node(
                    op_type="Slice",
                    inputs=[
                        node_pb.input[0],
                        starts_node.output[0],
                        ends_node.output[0],
                        axes_node.output[0],
                    ],
                    outputs=[node_pb.output[i]],
                    name=f"{node}/Slice{i}",
                )
                node_to_add.extend([starts_node, ends_node, axes_node, slice_node])
                starts += ch
            node_to_remove.append(node_pb)
    for node in node_to_add:
        graph.add_onnx_node(node)
    for node in node_to_remove:
        graph.remove_onnx_node(node)
    return graph
