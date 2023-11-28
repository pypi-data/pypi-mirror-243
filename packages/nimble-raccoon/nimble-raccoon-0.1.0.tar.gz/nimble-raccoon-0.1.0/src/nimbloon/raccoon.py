import os
from typing import Any, Optional, Union, Callable, Iterable

import numpy as np
import pandas as pd

from sklearn.metrics import silhouette_score as sils
from sklearn.preprocessing import StandardScaler as ss
from sknetwork.clustering import Louvain

from umap import UMAP

from loguru import logger
from datetime import datetime

from .utils import *
from .trees import build_tree


class Raccoon:
    """ Fast and slim version of RACCOON,
        an iterative multi-scale clustering algorithm.
    """

    def __init__(self, out_path: str = "./rc_output",
                 metric: str = "cosine",
                 scale: bool = False, 
                 cumulative_variance: Union[Iterable[float], float] = .9,
                 max_tsvd_components: Optional[int] = 1000,
                 target_dimensions: Optional[int] = 12,
                 n_neighbors: Union[Iterable[int], int, Callable] = np.sqrt,
                 clustering_parameter: Union[Iterable[float], float] = np.linspace(.1, 3, 50), 
                 min_cluster_size: int = 10,
                 max_neighbors: int = 100, 
                 silhouette_threshold: float = 0.,
                 max_depth: Optional[int] = None, 
                 random_state: Optional[int] = None) -> None:
        """ Initializes the RACCOON object.

        :param out_path: str, path where all output will be saved Default: "./rc_output".
        :param metric: str, metric to evaluate distances. Can either be "cosine" or "euclidean". Default: "cosine".
        :param scale: bool, whether to scale the input data. Default: False.
        :param cumulative_variance: Union[Iterable[float], float], 
            cumulative variance of principal components to be obtained with tSVD. Default: .9.
        :param max_tsvd_components: Optional[int], maximum number of components to use for dimensionality reduction. Default: None.
        :param target_dimensions: int, number of dimensions to reduce the data to with UMAP. Default: 12.
        :param n_neighbors: Union[Iterable[int], int, Callable], number of neighbors to use for the UMAP graph and KNN.
            If a function is provided, it will be applied to the total number of data points. Default: np.sqrt.
        :param clustering_parameter: Union[Iterable[float], float], parameter space to search for identifying the optimal clustering. 
            Default: np.linspace(.1, 3, 50).
        :param min_cluster_size: int, minimum number of members to perform clustering. Default: 2.
        :param max_neighbors: int, maximum number of neighbours to use for the SNN graph. Default: 100.
        :param silhouette_threshold: float, baseline silhouette score. Default: 0.
        :param max_depth: Optional[int], maximum number of levels to use for the clustering.  Starts at 0 for root search. Default: None.
        :param random_state: Optional[int], random state to use for reproducibility. Default: None.
        """

        self.random_state = random_state
        if self.random_state is not None:
            np.random.seed(self.random_state)

        self.out_path = out_path
        os.makedirs(os.path.join(self.out_path, "plots"), exist_ok=True)

        self._logger = logger
        self._logger.add(os.path.join(out_path, "rc_{}_{}.log".format(datetime.now().strftime('%Y%m%d'), os.getpid())))

        if not isinstance(cumulative_variance, Iterable):
            cumulative_variance = [cumulative_variance]
        if not isinstance(clustering_parameter, Iterable):
            clustering_parameter = [clustering_parameter]

        self._params_table = None

        if target_dimensions is not None and min_cluster_size <= target_dimensions:
            self._logger.warning("Minimum size of clusters is smaller or equal than target dimensions.\n"+ 
                                 "UMAP spectral initialization may be skipped in smaller clusters.")
            
        self.rc_args = {"metric": metric,
                        "scale" : scale,
                        "cumulative_variance" : cumulative_variance,
                        "max_tsvd_components" : max_tsvd_components,
                        "target_dimensions" : target_dimensions,
                        "n_neighbors" : n_neighbors,
                        "clustering_parameter" : clustering_parameter,
                        "min_cluster_size" : min_cluster_size,
                        "max_neighbors" : max_neighbors,
                        "silhouette_threshold" : silhouette_threshold,
                        "max_depth": max_depth}
        
    def __setattr__(self, __name: str, __value: Any) -> None:
        """ Sets the attributes of the RACCOON object.
        
        :param __name: str, name of the attribute.
        :param __value: Any, value of the attribute.
        """
        
        if 'rc_args' in self.__dict__ and __name in self.rc_args.keys():
            self.__dict__['rc_args'][__name] = __value
        else:
            self.__dict__[__name] = __value

    def _single_svd(self, 
                    input_data: pd.DataFrame,
                    cumulative_variance: float = .9,
                    max_tsvd_components: Optional[int] = 1000,
                    metric: str = "cosine",
                    ) -> np.ndarray:
        """ Performs low information filtering on the input data, using tSVD.

        :param input_data: pd.DataFrame, input data.
        :param cumulative_variance: float, cumulative variance of principal components to be obtained with tSVD. Default: .9.
        :param max_tsvd_components: Optional[int], maximum number of components to use for tSVD. Default: None.
        :param metric: str, metric to evaluate distances. Can either be "cosine" or "euclidean". Default: "cosine".
        :return: np.ndarray, data encoded in the selected principal components.
        """

        if cumulative_variance < 1:
            self._logger.info("Reducing cumulative variance to {:.2f}.".format(cumulative_variance))
            _, data_tsvd = svd_by_variance(
                input_data, cumulative_variance=cumulative_variance, max_components=max_tsvd_components,
                    random_state=self.random_state)
        else:
            self._logger.info("Cumulative variance was set to 1. Skipping SVD.")
            data_tsvd = input_data.values.astype(np.float32)

        if metric == "cosine":
            self._logger.info("Scaling tSVD entries to unit norm.")
            data_tsvd /= np.linalg.norm(data_tsvd, axis=1, keepdims=True)

        return data_tsvd
    
    def _single_umap(self,
                    input_data: pd.DataFrame,
                    target_dimensions: Optional[int] = 12,
                    n_neighbors: Union[int, Callable] = np.sqrt,
                    metric: str = "cosine",
                    ) -> tuple[np.ndarray, np.ndarray]:
        """ Performs dimensionality reduction on the input data, using UMAP.

        :param input_data: pd.DataFrame, input data.
        :param target_dimensions: int, number of dimensions to reduce the data to with UMAP. Default: 12.
        :param n_neighbors: Union[int, Callable], number of neighbors to use for the UMAP graph and KNN. 
            If a function is provided, it will be applied to the total number of data points. Default: np.sqrt.
        :param metric: str, metric to evaluate distances. Can either be "cosine" or "euclidean". Default: "cosine".
        :return: tuple(np.ndarray, np.ndarray), umap projection and indices of the nearest neighbors.
        """

        nn_dists, nn_ixs = nn_faiss(input_data, None, metric=metric, n_neighbors=n_neighbors)

        if target_dimensions != None:
            self._logger.info("Reducing dimensions to {:d} with UMAP.".format(target_dimensions))

            data_umap = UMAP(precomputed_knn = (nn_ixs, 1-nn_dists, DummyNNDescent()),
                            n_components=target_dimensions, n_neighbors=n_neighbors, metric=metric,
                            random_state=self.random_state, 
                            init="spectral" if input_data.shape[0] > target_dimensions else "random",
                            **Constants.umap_params).fit_transform(input_data)

            if metric == "cosine":
                self._logger.info("Scaling UMAP entries to unit norm.")
                data_umap /= np.linalg.norm(data_umap, axis=1, keepdims=True)

            nn_dists, nn_ixs = nn_faiss(data_umap, None, metric=metric, n_neighbors=n_neighbors)

        else:
            self._logger.info("Reduced dimensions was set to None. Skipping UMAP.")
            data_umap = input_data
            nn_dists, nn_ixs = nn_dists, nn_ixs
        
        return data_umap, nn_ixs, 


    def _single_iteration(self, input_data: pd.DataFrame,
                    name: str = "0",
                    metric: str = "cosine",
                    scale: bool = False, 
                    cumulative_variance: Union[Iterable[float], float] = .9,
                    max_tsvd_components: Optional[int] = 1000,
                    target_dimensions: Optional[int] = 12,
                    n_neighbors: Union[Iterable[int], int, Callable] = np.sqrt,
                    clustering_parameter: Union[Iterable[float], float] = np.linspace(.1, 3, 50), 
                    min_cluster_size: int = 10,
                    max_neighbors: int = 100, 
                    silhouette_threshold: float = 0.,
                    max_depth: Optional[int] = None) -> pd.Series:
        """ Performs clustering on the input data iteratively.

        :param input_data: pd.DataFrame, input data.
        :param name: str, name of the output file. Default: "0".
        :param metric: str, metric to evaluate distances. Can either be "cosine" or "euclidean". Default: "cosine".
        :param scale: bool, whether to scale the input data. Default: False.
        :param cumulative_variance: Union[Iterable[float], float], 
            cumulative variance of principal components to be obtained with tSVD. Default: .9.
        :param max_tsvd_components: Optional[int], maximum number of components to use for dimensionality reduction. Default: None.
        :param target_dimensions: int, number of dimensions to reduce the data to with UMAP. Default: 12.
        :param n_neighbors: Union[Iterable[int], int, Callable], number of neighbors to use for the UMAP graph and KNN.
            If a function is provided, it will be applied to the total number of data points. Default: np.sqrt.
        :param clustering_parameter: Union[Iterable[float], float], parameter space to search for identifying the optimal clustering. 
            Default: np.linspace(.1, 3, 50).
        :param min_cluster_size: int, minimum number of members to perform clustering. Default: 10.
        :param max_neighbors: int, maximum number of neighbours to use for the SNN graph. Default: 100.
        :param silhouette_threshold: float, baseline silhouette score. Default: 0.
        :param max_depth: Optional[int], maximum number of levels to use for the clustering.  Starts at 0 for root search. Default: None.
        :return: pd.Series, labels.
        """

        if max_depth is not None and  name.count("_") > max_depth:
            self._params_table.write("{:s},{:d},{:d},{:.3f},{:.3f},{:d},{:s}\n".format(
                name, input_data.shape[1], 0, np.nan, np.nan, 0, "maximum depth reached"))
            return pd.Series(np.zeros(input_data.shape[0]), index=input_data.index, name=name).astype(int)

        if input_data.shape[0] <= min_cluster_size:
            self._params_table.write("{:s},{:d},{:d},{:.3f},{:.3f},{:d},{:s}\n".format(
                name, input_data.shape[1], 0, np.nan, np.nan, 0, "too few members"))
            return pd.Series(np.zeros(input_data.shape[0]), index=input_data.index, name=name).astype(int)

        self._logger.info("Using {} cumulative variance thresholds.".format(cumulative_variance))

        if isinstance(n_neighbors, Callable):
            n_neighbors = n_neighbors(input_data.shape[0])
        if not isinstance(n_neighbors, Iterable):
            n_neighbors = [n_neighbors]
        n_neighbors = sorted(set([int(max(min(nn, max_neighbors),2)) for nn in n_neighbors]))
        self._logger.info("Using {} nearest neighbors.".format(n_neighbors))

        if scale:
            self._logger.info("Scaling features.")
            scaler = ss()
            scaler.fit(input_data)
            input_data = pd.DataFrame(scaler.transform(input_data),
                                    index=input_data.index, columns=input_data.columns)

        best_results = {'silhouette_score': silhouette_threshold,
                        'cumulative_variance': np.nan,
                        'n_neighbors': np.nan,
                        'clustering_parameter': np.nan,
                        'labels': [0]*input_data.shape[0],
                        'silhouette_list': [np.nan]*len(clustering_parameter),
                        'was_updated': False
                        }
            
        for cv in cumulative_variance:

            data_tsvd = self._single_svd(input_data,
                                         cumulative_variance=cv,
                                         max_tsvd_components=max_tsvd_components,
                                         metric=metric)
            
            for nn in n_neighbors:
         
                _, nn_ixs_u = self._single_umap(data_tsvd,
                                                target_dimensions=target_dimensions,
                                                n_neighbors=nn,
                                                metric=metric)

                self._logger.info("Calculating SNN matrix.")
                snn_mat = snn(searchable_set=nn_ixs_u, 
                            query_points=None,
                            metric="precomputed",
                            n_neighbors=nn,
                            logger=self._logger)

                sil_list = []
                self._logger.info("Clustering.")
                for cp in clustering_parameter:
                    self._logger.info("Clustering with parameter: {:.3f}".format(cp))
                    try:
                        labels = Louvain(resolution=cp).fit_predict(snn_mat)
                        sil = sils(1-snn_mat, labels, metric="precomputed")
                        sil_list.append(sil)
                        if sil > best_results['silhouette_score']:
                            best_results['silhouette_score'] = sil
                            best_results['cumulative_variance'] = cv
                            best_results['n_neighbors'] = nn
                            best_results['clustering_parameter'] = cp
                            best_results['labels'] = labels
                            best_results['silhouette_list'] = sil_list
                            best_results['was_updated'] = True
                    except ValueError:
                        sil_list.append(silhouette_threshold)

        if best_results['was_updated']:
            plot_silhouette(clustering_parameter, best_results['silhouette_list'], os.path.join(
                self.out_path, "plots", "silhouette.{:s}_{:.3f}_{:.3f}.pdf".format(
                    name, best_results['cumulative_variance'], best_results['n_neighbors'])))
            best_results['was_updated']=False

        if best_results['silhouette_score'] == silhouette_threshold:
            self._logger.info("No optimal parameter found, skipping.")
            self._params_table.write("{:s},{:.3f},{:.3f},{:.3f},{:.3f},{:d},{:s}\n".format(
                name, np.nan, np.nan, np.nan, np.nan, 0, "no optimal parameters found"))
            return pd.Series(np.zeros(input_data.shape[0]), index=input_data.index, name=name).astype(int)
        else:
            for printable in ['cumulative_variance', 'n_neighbors', 'clustering_parameter', 'silhouette_score']:
                self._logger.info("Best {:s}: {:.2f}".format(printable.replace('_',' '), best_results[printable]))
                
        best_results['labels'] = pd.Series(
            best_results['labels'], index=input_data.index, name=name).astype(int)
        
        self._params_table.write("{:s},{:.3f},{:d},{:.3f},{:.3f},{:d},{:s}\n".format(
            name, best_results['cumulative_variance'], best_results['n_neighbors'],
            best_results['clustering_parameter'], best_results['silhouette_score'],
            best_results['labels'].nunique(), ""))
        
        return best_results['labels']


    def _iterate(self, input_data: pd.DataFrame, 
                        name: str = "0") -> pd.DataFrame:
        """ Performs iterative clustering on the input data, using the Raccoon algorithm.

        :param input_data: pd.DataFrame, input data.
        :param name: str, name of the output file. Default: "0".
        :return: pd.DataFrame, labels.
        """

        self._logger.info("Working on cluster {} with {:d} samples.".format(
            name, input_data.shape[0]))

        labels = self._single_iteration(input_data,
                                name=name,
                                **self.rc_args)

        sublabels = [self._iterate(input_data.loc[labels == label, :],
                                    name='{}_{}'.format(name, label))
                    for label in labels.unique()] if labels.max() > 0 else []
        labels = pd.concat([labels] + sublabels, axis=1)
        labels.columns = labels.columns.astype(str)

        return labels[sorted(labels.columns)]

    def __call__(self, input_data: pd.DataFrame,
                    name: str = "0") -> tuple[pd.DataFrame, list]:
        """ Runs a full cycle of the Raccoon algorithm.

        :param input_data: pd.DataFrame, input data.
        :param name: str, name of the output file. Default: "0".
        :return: tuple(pd.DataFrame, list), clusters and hierarchical tree.
        """

        print_header()
        
        self._params_table = open(os.path.join(self.out_path, 'params.csv'), 'w')
        self._params_table.write("name,npc,nn,cparm,sil,nclu,notes\n")

        labels = self._iterate(input_data, name=name).fillna(-1).astype(int)
        
        self._params_table.close()
        self._params_table = None

        labels.to_parquet(os.path.join(self.out_path, 'rc_results.pq'))
        tree = build_tree(labels, os.path.join(self.out_path, 'rc_tree.json'))

        self._logger.info('All done!')

        return labels, tree
    