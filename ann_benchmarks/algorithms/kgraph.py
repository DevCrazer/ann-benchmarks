from __future__ import absolute_import
import os
import numpy
import pykgraph
from ann_benchmarks.constants import INDEX_DIR
from ann_benchmarks.algorithms.base import BaseANN

class KGraph(BaseANN):
    def __init__(self, metric, P, index_params, save_index):
        self.name = 'KGraph(%s,P=%d)' % (metric, P)
        self._P = P
        self._metric = metric
        self._index_params = index_params
        self._save_index = save_index

    def fit(self, X):
        X = numpy.array(X)
        if X.dtype != numpy.float32:
            X = X.astype(numpy.float32)
        self._kgraph = pykgraph.KGraph(X, self._metric)
        path = os.path.join(INDEX_DIR, 'kgraph-index-%s' % self._metric)
        if os.path.exists(path):
            self._kgraph.load(path)
        else:
            self._kgraph.build(**self._index_params) #iterations=30, L=100, delta=0.002, recall=0.99, K=25)
            if not os.path.exists(INDEX_DIR):
              os.makedirs(INDEX_DIR)
            self._kgraph.save(path)

    def query(self, v, n):
        if v.dtype != numpy.float32:
            v = v.astype(numpy.float32)
        result = self._kgraph.search(numpy.array([v]), K=n, threads=1, P=self._P)
        return result[0]
