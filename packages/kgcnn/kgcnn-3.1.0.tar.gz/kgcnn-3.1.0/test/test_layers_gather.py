import unittest

import numpy as np
import tensorflow as tf
from kgcnn.data.base import MemoryGraphDataset
from kgcnn.layers.gather import GatherEdgesPairs
from kgcnn.layers.gather import GatherNodes


class TestGather(unittest.TestCase):

    n1 = [[[1.0], [6.0], [1.0], [6.0], [1.0], [1.0], [6.0], [6.0]],
          [[6.0], [1.0], [1.0], [1.0], [7.0], [1.0], [6.0], [8.0], [6.0], [1.0], [6.0], [7.0], [1.0], [1.0], [1.0]]]
    ei1 = [[[0, 1], [1, 0], [1, 6], [2, 3], [3, 2], [3, 5], [3, 7], [4, 7], [5, 3], [6, 1], [6, 7], [7, 3], [7, 4],
            [7, 6]],
           [[0, 6], [0, 8], [0, 9], [1, 11], [2, 4], [3, 4], [4, 2], [4, 3], [4, 6], [5, 10], [6, 0], [6, 4], [6, 14],
            [7, 8], [8, 0], [8, 7], [8, 11], [9, 0], [10, 5], [10, 11], [10, 12], [10, 13], [11, 1], [11, 8], [11, 10],
            [12, 10], [13, 10], [14, 6]]]
    e1 = [[[0.408248290463863], [0.408248290463863], [0.3333333333333334], [0.35355339059327373], [0.35355339059327373],
           [0.35355339059327373], [0.25], [0.35355339059327373], [0.35355339059327373], [0.3333333333333334],
           [0.2886751345948129], [0.25], [0.35355339059327373], [0.2886751345948129]],
          [[0.25], [0.25], [0.35355339059327373], [0.35355339059327373], [0.35355339059327373], [0.35355339059327373],
           [0.35355339059327373], [0.35355339059327373], [0.25], [0.3162277660168379], [0.25], [0.25],
           [0.35355339059327373], [0.35355339059327373], [0.25], [0.35355339059327373], [0.25], [0.35355339059327373],
           [0.3162277660168379], [0.22360679774997896], [0.3162277660168379], [0.3162277660168379],
           [0.35355339059327373], [0.25], [0.22360679774997896], [0.3162277660168379], [0.3162277660168379],
           [0.35355339059327373]]]

    def test_gather_nodes_concat(self):
        node = tf.ragged.constant(self.n1, ragged_rank=1, inner_shape=(1,))
        edgeind = tf.ragged.constant(self.ei1, ragged_rank=1, inner_shape=(2,))

        gathered_nodes_concat = GatherNodes()([node, edgeind])
        np_gather = np.reshape(np.array(self.n1[1])[np.array(self.ei1[1])],(28,2*1))
        test = np.sum(np.abs(np.array(gathered_nodes_concat[1]) - np_gather)) < 1e-6
        self.assertTrue(test)

    def test_gather_nodes(self):
        node = tf.ragged.constant(self.n1, ragged_rank=1, inner_shape=(1,))
        edgeind = tf.ragged.constant(self.ei1, ragged_rank=1, inner_shape=(2,))

        gathered_nodes = GatherNodes(concat_axis=None, split_axis=None)([node, edgeind])
        np_gather = np.array(self.n1[1])[np.array(self.ei1[1])]
        test = np.sum(np.abs(np.array(gathered_nodes[1]) - np_gather)) < 1e-6
        self.assertTrue(test)

    # def test_gather_empty(self):
    #     node = tf.ragged.constant(self.n1, ragged_rank=1, inner_shape=(1,))
    #
    #     ei2 = tf.RaggedTensor.from_row_lengths(tf.constant([],dtype=tf.int64),tf.constant([0,0],dtype=tf.int64))
    #     gather_empty = GatherNodes(concat_axis=False)([node,ei2])
    #     gather_empty_concat = GatherNodes(concat_axis=True)([node, ei2])


class TestReverseEdges(unittest.TestCase):
    n1 = [[[2.0], [3.0], [4.0]], [[1.0], [10.0], [100.0]]]
    ei1 = [[[0, 1], [1, 0], [1, 2], [2, 1]], [[0, 1], [1, 2], [2, 1], [2, 0]]]
    e1 = [[[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]],
          [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]]]

    def test_gather(self):
        edge = tf.ragged.constant(self.e1, ragged_rank=1, inner_shape=(2,))
        edgeind = tf.ragged.constant(self.ei1, ragged_rank=1, inner_shape=(2,))
        ds = MemoryGraphDataset()
        ds.set("edge_indices", [np.array(self.ei1[0]), np.array(self.ei1[1])])
        ds.map_list(method="set_edge_indices_reverse")
        edge_pair = tf.RaggedTensor.from_row_lengths(np.concatenate(ds.get("edge_indices_reverse"), axis=0),
                                                     [len(x) for x in ds.get("edge_indices_reverse")])
        edges_gather = GatherEdgesPairs()([edge, edge_pair])
        result = edges_gather

        self.assertTrue(
            np.amax(np.abs(np.array(result[0]) - np.array([[1.0, 1.0], [0.0, 0.0], [3.0, 3.0], [2.0, 2.0]]))) < 1e-4)

        # layer.get_config()


if __name__ == '__main__':
    unittest.main()