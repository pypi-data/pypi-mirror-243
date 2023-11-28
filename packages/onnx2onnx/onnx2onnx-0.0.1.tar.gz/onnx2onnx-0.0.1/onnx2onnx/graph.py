"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

import os
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

import networkx as nx
import numpy as np
import onnx
from onnx import numpy_helper


class OnnxGraph(nx.DiGraph):
    """Create a DAG from onnx graph."""

    def __init__(self, model: onnx.ModelProto) -> None:
        super().__init__(name=model.graph.name)
        self._model = model
        self._node_to_out = {}
        graph = onnx.shape_inference.infer_shapes(model).graph
        self.inputs = [i.name for i in graph.input]
        self.outputs = [i.name for i in graph.output]
        for node in graph.node:
            self._add_onnx_node_internal(node)
        self._build_edges()

    def _add_onnx_node_internal(self, node: onnx.NodeProto) -> None:
        assert node.HasField("name")
        name = node.name
        has_input = any(i in self.inputs for i in node.input)
        has_output = any(i in self.outputs for i in node.output)
        self.add_node(name, pb=node, has_input=has_input, has_output=has_output)
        self._node_to_out[name] = node.output

    def _build_edges(self):
        out_to_node = {i: k for k, v in self._node_to_out.items() for i in v}
        for n in self.nodes:
            node = self.nodes[n]["pb"]
            for i in node.input:
                if upstream := out_to_node.get(i):
                    self.add_edge(upstream, n)

    def add_onnx_node(self, node: onnx.NodeProto) -> None:
        """Insert a node and its edges."""
        self._add_onnx_node_internal(node)
        self._build_edges()

    def remove_onnx_node(self, node: onnx.NodeProto) -> None:
        """Remove a node from the graph"""
        if node.name not in self:
            raise ValueError(f"Node {node.name} is not existing in the graph!")
        self.remove_node(node.name)

    def onnx_predecessors(self, n: onnx.NodeProto) -> List[onnx.NodeProto]:
        """Returns a list of predecessor nodes of n."""
        preds = self.predecessors(n.name)
        return [self.nodes[p]["pb"] for p in preds]

    def onnx_successors(self, n: onnx.NodeProto) -> List[onnx.NodeProto]:
        """Returns a list of successors nodes of n."""
        succs = self.successors(n.name)
        return [self.nodes[s]["pb"] for s in succs]

    def constants(self, n: onnx.NodeProto) -> List[np.ndarray]:
        """Get constant inputs of n."""
        const = []
        for pred in self.onnx_predecessors(n):
            if pred.op_type == "Constant":
                const.append(numpy_helper.to_array(pred.attribute[0].t))
        return const

    @property
    def input(self) -> List[onnx.ValueInfoProto]:
        """Return a list of graph inputs value info."""
        return self._model.graph.input

    @property
    def output(self) -> List[onnx.ValueInfoProto]:
        """Return a list of graph outputs value info."""
        return self._model.graph.output

    @property
    def initializer(self) -> List[onnx.TensorProto]:
        """Return a list of graph initializer tensors."""
        return self._model.graph.initializer

    @property
    def model(self) -> onnx.ModelProto:
        """Make new model"""
        graph = deepcopy(self._model.graph)
        graph.ClearField("node")
        for n in nx.topological_sort(self):
            graph.node.append(self.nodes[n]["pb"])
        model = onnx.helper.make_model(
            graph,
            doc_string=self._model.doc_string,
            domain=self._model.domain,
            model_version=self._model.model_version,
            opset_imports=self._model.opset_import,
            producer_name=self._model.producer_name,
            producer_version=self._model.producer_version,
        )
        model.metadata_props.extend(self._model.metadata_props)
        return model

    # pylint: disable=redefined-builtin
    def save(self, model_path: str | os.PathLike, format: Optional[str] = None):
        """Serialize the graph to onnx model and save to model_path."""
        model = self.model
        if format == "protobuf" or format is None:
            model_path = Path(model_path).with_suffix(".onnx")
        elif format == "textproto":
            model_path = Path(model_path).with_suffix(".pbtxt")
        elif format == "json":
            model_path = Path(model_path).with_suffix(".json")
        elif format == "onnxtxt":
            model_path = Path(model_path).with_suffix(".onnxtxt")
        onnx.checker.check_model(model, full_check=True)
        onnx.save_model(model, model_path, format=format)
