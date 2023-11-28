import os

from typing import Optional

from copy import deepcopy

import numpy as np
import pandas as pd

from sklearn.decomposition import TruncatedSVD as tsvd
from scipy.sparse import csr_matrix

import pynndescent 

import faiss

import matplotlib.pyplot as plt

from tqdm import tqdm
from loguru import logger

class Constants:
    """ Class to store all the constants used in the project. """

    umap_params = {'min_dist': 0.1, 'spread': 1,
                  'n_epochs': 500, 'learning_rate': 0.1,
                  'verbose': False}


class DummyNNDescent(pynndescent.NNDescent):
    """ Dummy class forcing UMAP to accept a precomputed NN tuple. 
    
    Reference issues:
        https://github.com/lmcinnes/umap/issues/848
        https://github.com/lmcinnes/umap/issues/926
    """

    def __init__(self):
        return None
    

def svd_by_variance(df: pd.DataFrame, cumulative_variance: float = .99,
                    max_components: Optional[int] = None, 
                    random_state: Optional[int] = None) -> tuple[tsvd, np.ndarray]:
    """ Performs truncated SVD on a dataframe, keeping only the components
    that explain a given amount of variance.

    :param df: dataframe, the dataframe to perform SVD on.
    :param cumulative_variance: float, the amount of variance to explain.
    :param max_components: int, the maximum number of components to consider.
    :return: tuple, the SVD object and the transformed dataframe.
    """

    if max_components is None or df.shape[1]<max_components:
        max_components = df.shape[1]

    svd = tsvd(n_components=max_components,
               random_state=random_state)
    svd.fit(df)

    evr = svd.explained_variance_ratio_
    cutoff = sum(np.cumsum(evr) <= cumulative_variance)
    if cutoff < 2:
        cutoff = 2
    print("tSVD: keeping {:d} components to reach {:.3f} cumulative variance".format(
        cutoff, np.cumsum(evr)[cutoff-1]))

    svd.n_components = cutoff
    svd.components_ = svd.components_[:svd.n_components, :]
    svd.explained_variance_ = svd.explained_variance_[:svd.n_components]

    return svd, svd.transform(df).astype(np.float32)


def nn_faiss(searchable_set: np.array,
             query_points: Optional[np.array] = None,
             metric: str = "cosine",
             n_neighbors: Optional[int] = None) -> tuple[np.array]:
    """ Finds the nearest neighbors of a set of query points in a searchable set.

    :param searchable_set: array, searchable set of samples x features, from which the neighbors will be pooled.
    :param query_points: array, query points of samples x features. If None, will be set to searchable_set.
    :param metric: str, metric to evaluate distances. Can either be "cosine" or "euclidean". Default: "cosine".
    :param n_neighbors: int, number of neighbors to return.
    :return: tuple, distances and indices of the nearest neighbors, of shape query_points x neighbors.
    """

    if metric == "cosine":
        index_function = faiss.IndexFlatIP
    elif metric == "euclidean":
        index_function = faiss.IndexFlatL2
    else:
        logger.error('Metric must be either "cosine" or "euclidean".')
        raise ValueError(
            'Metric must be either "cosine" or "euclidean".')

    if query_points is None:
        query_points = searchable_set
    else:
        if searchable_set.shape[1] != query_points.shape[1]:
            raise ValueError(
                'Searchable set and query points must have the same number of features.')

    index = index_function(searchable_set.shape[1])
    index.add(searchable_set)
    return index.search(query_points, k=n_neighbors if n_neighbors is not None
                        else int(np.sqrt(searchable_set.shape[0])))


def snn(searchable_set: np.array,
        query_points: Optional[np.array] = None,
        metric: str = "cosine",
        n_neighbors: Optional[int] = None,
        low_mem: bool = False,
        logger: Optional[type(logger)] = None,
        verbose: bool = True) -> np.ndarray:
    """ Calculates Shared Nearest Neighbor (SNN) matrix with faiss
    https://github.com/facebookresearch/faiss/wiki/Faiss-indexes

    Note: I tried multiprocessing but it is not worth it (it is actually slower).

    :param searchable_set: array, searchable set of samples x features, from which the neighbors will be pooled.
    :param query_points: array, query points of samples x features. If None, will be set to searchable_set.
    :param metric: str, metric to evaluate distances. Can either be "cosine", "euclidean" or "precomputed". 
        If "precomputed" values need to be a np.array of shape data_points x n_neighbors with the 
        indices of the nearest neighbors. Default: "cosine".
    :param n_neighbors: int, number of neighbors to use for SNN calculation. Default: None.
        If None, will be set to sqrt(n_samples).
    :param low_mem: bool, whether to return a sparse matrix. Default: False.
    :return: array, SNN matrix.
    """

    print_function = logger.info if logger is not None else print

    n_neighbors = int(np.sqrt(
        searchable_set.shape[0])) if n_neighbors is None else n_neighbors

    offset = 0

    if metric == "precomputed":
        print_function('Running SNN with precomputed NN indices.'+\
                       'query_points parameter will be ignored.')
        nn_ixs = searchable_set
    else:
        if query_points is None:
            query_points = searchable_set
        else:
            if searchable_set.shape[1] != query_points.shape[1]:
                raise ValueError(
                    'Searchable set and query points must have the same number of features.')
            query_points = np.concatenate([searchable_set, query_points])
            offset = searchable_set.shape[0]
    
        print_function('Finding nearest neighbors.')
        _, nn_ixs = nn_faiss(searchable_set, query_points,
                         metric=metric, n_neighbors=n_neighbors)

    neighborhoods = [set(ixs) for ixs in nn_ixs]

    if verbose:
        print_function('Symmetrizing neighborhoods.')
    query_neighborhoods = deepcopy(neighborhoods)
    for i, n in tqdm(enumerate(neighborhoods), total=len(neighborhoods), disable= not verbose):
        for _, s in enumerate(n):
            query_neighborhoods[s].update({i})      
        if i==offset-1:
            break     

    if verbose:
        print_function('Finding second degree symetric neighbors.')
    query_neighborhoods = [first_nn_list | set([second_nn for first_nn in first_nn_list
                                                for second_nn in query_neighborhoods[first_nn]])
                           for _, first_nn_list in tqdm(enumerate(query_neighborhoods[offset:]),
                                                        total=len(query_neighborhoods[offset:]), disable= not verbose)]

    if verbose:
        print_function('Initializing matrix.')
    shared_neighbors = np.zeros(
        (len(query_neighborhoods), searchable_set.shape[0]), dtype=np.uint16)

    if verbose:
        print_function('Evaluating intersections.')
    for i, sn in tqdm(enumerate(query_neighborhoods), total=len(query_neighborhoods), disable= not verbose):
        for _, s in enumerate(sn):
            shared_neighbors[i, s] = len(
                neighborhoods[i+offset].intersection(neighborhoods[s]))

    return csr_matrix(shared_neighbors) if low_mem else shared_neighbors


def plot_silhouette(params: list[float], scores: list[float], save_path: Optional[str] = None) -> None:
    """ Plots a line plot with the silhouette performance over the search.

    :param params: list, list of parameters.
    :param scores: list, list of silhouette scores.
    :param save_path: str, path to save the plot. Default: None.
    """

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)

    ax.set_facecolor('white')
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)

    ceiling = np.nanmax(scores)
    floor = np.nanmin(scores)

    if np.isnan(ceiling):
        return None

    plt.plot(params, scores, lw=1.5, color='#444444', marker='.', markersize=10)
    plt.scatter([params[np.nanargmax(scores)]], [scores[np.nanargmax(scores)]], s=150, lw=1.5, edgecolors='#FF4444', facecolors='none')
    
    plt.xticks(params, fontsize=10, rotation=90)
    plt.xlabel('Parameter', fontsize=20)

    plt.ylim(floor -.1, ceiling + .1)
    plt.yticks(np.linspace(floor, ceiling, 5), ['{:.2f}'.format(x) for x in np.linspace(floor, ceiling, 5)], fontsize=15)
    plt.ylabel('Silhouette\nscores', fontsize=20, rotation=90)

    ax.tick_params(axis=u'both', which=u'both', length=0)

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path)

def print_header() -> None:
    
    with open(os.path.join(os.path.dirname(__file__), 'static', 'header.txt'), 'r') as file:
        for line in file.readlines():
            print(line, end='')
            