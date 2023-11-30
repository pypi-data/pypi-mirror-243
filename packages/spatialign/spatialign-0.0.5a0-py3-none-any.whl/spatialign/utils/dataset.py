#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/9/23 5:16 PM
# @Author  : zhangchao
# @File    : dataset.py
# @Email   : zhangchao5@genomics.cn
import scanpy as sc
import torch
import scipy.sparse as sp
import torch_geometric

from anndata import AnnData
from torch_geometric.data import Data
from torch_geometric.utils import to_undirected

from spatialign.utils import get_format_time


class Dataset:
    """
    Multiple dataset loading, preprocessing and convert to dataloader
    :param adata: AnnData
        Input dataset path.
    :param batch_key: str
        the batch annotation to :attr:`obs` using this key, default, 'batch'.
    :param is_hvg: bool
        Whether to perform 'sc.pp.highly_variable_genes' processing, default, False.
    :param is_reduce: bool
        Whether to perform PCA reduce dimensional processing, default, False.
    :param n_pcs: int
        PCA dimension reduction parameter, valid when 'is_reduce' is True, default, 100.
    :param n_hvg: int
        'sc.pp.highly_variable_genes' parameter, valid when 'is_reduce' is True, default, 2000.
    :param n_neigh: int
        The number of neighbors selected when constructing a spatial neighbor graph. default, 15.
    :param is_undirected: bool
        Whether the constructed spatial neighbor graph is undirected graph, default, True.
    """

    def __init__(self,
                 adata: AnnData,
                 batch_key: str = "batch",
                 is_hvg: bool = False,
                 is_reduce: bool = False,
                 n_pcs: int = 100,
                 n_hvg: int = 2000,
                 n_neigh: int = 15,
                 is_undirected: bool = True):

        self.batch_key = batch_key
        self.merge_data, self.loader_list = self.get_loader(adata, is_reduce=is_reduce, is_hvg=is_hvg, n_pcs=n_pcs,
                                                            n_hvg=n_hvg, n_neigh=n_neigh, is_undirected=is_undirected)
        self.n_domain = self.merge_data.obs[batch_key].cat.categories.size
        self.n_node = self.merge_data.shape[0]

        self.inner_dims = n_pcs if is_reduce else self.merge_data.shape[1]
        self.inner_genes = self.merge_data.var_names.tolist()

    def get_loader(self,
                   merge_data,
                   is_reduce=False,
                   is_hvg=False,
                   n_pcs=50,
                   n_hvg=2000,
                   n_neigh=30,
                   is_undirected=True):
        if is_hvg:
            sc.pp.highly_variable_genes(merge_data, flavor="seurat_v3", n_top_genes=n_hvg)
            merge_data = merge_data[:, merge_data.var["highly_variable"]]

        dataset_list = self._loader(
            merge_data=merge_data, is_reduce=is_reduce, n_pcs=n_pcs, n_neigh=n_neigh, is_undirected=is_undirected)
        return merge_data, dataset_list

    def convert_tensor(self, data, q=50, is_reduce=False):
        data = data if not sp.issparse(data) else data.toarray()
        x_tensor = torch.tensor(data)
        if not is_reduce:
            return x_tensor
        else:
            u, s, v = torch.pca_lowrank(x_tensor, q=q)
            pca_tensor = torch.matmul(x_tensor, v)
            return pca_tensor

    def _loader(self, merge_data, is_reduce=False, n_pcs=100, n_neigh=15, is_undirected=True):
        dataset_list = []
        if "spatial" in merge_data.obsm_keys():
            print(f"{get_format_time()}: Spatial coordinates are used to calculate nearest neighbor graphs")
            spatial_key = "spatial"
        else:
            print(f"{get_format_time()}: PCA embedding are used to calculate nearest neighbor graphs")
            spatial_key = "pca"

        for d_idx, domain in enumerate(merge_data.obs[self.batch_key].cat.categories):
            data = merge_data[merge_data.obs[self.batch_key] == domain]
            feat_tensor = self.convert_tensor(data.X, q=n_pcs, is_reduce=is_reduce)

            if spatial_key == "spatial":
                dataset = Data(x=feat_tensor, pos=torch.Tensor(data.obsm[spatial_key]))
            else:
                pos_tensor = self.convert_tensor(data=data.X, q=10, is_reduce=True)
                dataset = Data(x=feat_tensor, pos=pos_tensor)

            dataset = torch_geometric.transforms.KNNGraph(k=n_neigh, loop=True)(dataset)
            dataset.edge_weight = torch.ones(dataset.edge_index.size(1))
            dataset.neigh_graph = torch.zeros((dataset.num_nodes, dataset.num_nodes), dtype=torch.float)
            dataset.neigh_graph[dataset.edge_index[0], dataset.edge_index[1]] = 1.
            if is_undirected:
                dataset.edge_index, dataset.edge_weight = to_undirected(dataset.edge_index, dataset.edge_weight)
                dataset.edge_weight = torch.ones_like(dataset.edge_weight)
            dataset.domain_idx = torch.tensor([d_idx] * data.shape[0], dtype=torch.int32)
            dataset.idx = torch.tensor(range(data.shape[0]), dtype=torch.int32)
            dataset_list.append(dataset)
        return dataset_list


def reader(*data_path, min_cells=20, min_genes=20, is_norm_log=True, is_scale=False, batch_key="batch"):
    print(f"{get_format_time()} Found Dataset: ")
    data_list = []
    for path in data_path:
        data = sc.read_h5ad(path)
        data.var_names_make_unique()
        data.obs_names_make_unique()

        if is_norm_log:
            sc.pp.filter_cells(data, min_genes=min_genes)
            sc.pp.filter_genes(data, min_cells=min_cells)
            sc.pp.normalize_total(data, target_sum=1e4)
            sc.pp.log1p(data)
        if is_scale:
            sc.pp.scale(data, zero_center=False, max_value=10)

        data_list.append(data)
    [print(f"  cell nums: {data.shape[0]} gene nums: {data.shape[1]}") for data in data_list]
    if len(data_path) > 1:
        merge_data = AnnData.concatenate(*data_list, batch_key=batch_key)
    else:
        merge_data = data_list[0]
        merge_data.obs[batch_key] = 0
        merge_data.obs[batch_key] = merge_data.obs[batch_key].astype("category")
    return merge_data
