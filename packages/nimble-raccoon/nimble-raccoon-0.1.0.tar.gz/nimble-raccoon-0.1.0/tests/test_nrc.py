import os
import shutil
import sys

import hashlib
import base64

from pandas.testing import assert_frame_equal

import numpy as np
import pandas as pd

import pytest

from nimbloon import Raccoon
from nimbloon.trees import load_tree

from anytree import Node

input_path = os.path.join("./tests")
assert os.path.exists(input_path)

np.random.seed(32)
dummy_data = pd.DataFrame(np.random.rand(250,50))


def assert_tree_equal(tree_one: Node, tree_two: Node) -> None:
    
    for node_one, node_two in zip(tree_one.descendants, tree_two.descendants):
        
        assert node_one.name == node_two.name
        assert node_one.parent.name == node_two.parent.name
        assert node_one.population == node_two.population
        assert node_one.level == node_two.level
        assert node_one.leaf == node_two.leaf
        for child_one, child_two in zip(node_one.children, node_two.children):
            assert child_one.name == child_two.name



@pytest.mark.parametrize("metric,scale,cumulative_variance,n_neighbors,target_dimensions", 
                         [("cosine", True, 1, np.sqrt, None),
                          ("cosine", False, .999, [8, 15], 12),
                          ("euclidean", False, .999, [8, 15], 12)])
class TestRaccoon:
    """ Test full raccoon pipeline. """

    @pytest.fixture()
    def rc_args(self, metric, scale, cumulative_variance, n_neighbors, target_dimensions) -> dict:
        """ Set raccoon parameters. """
        
        return {'metric': metric,
            'scale' : scale,
            'cumulative_variance' : cumulative_variance,
            'max_tsvd_components': 49,
            'clustering_parameter' : [.25,.1],
            'n_neighbors' : n_neighbors,
            'target_dimensions': target_dimensions,
            'max_neighbors' : 10,
            'min_cluster_size' : 25,
            'silhouette_threshold' : -.5,
            'max_depth': 2,
            'random_state': 32}   
        
    @pytest.fixture()
    def hashed_name(self, rc_args: dict) -> str:
        """ Define a hash string for files written to disk. """
        
        return base64.urlsafe_b64encode(hashlib.md5(''.join([str(val) for val in rc_args.values()])\
            .encode('utf-8')).digest()).decode('ascii') 

    @pytest.fixture()
    def raccoon(self, rc_args: dict, tmpdir) -> Raccoon:
        """ Set up a rc object """

        rc = Raccoon(out_path=tmpdir, **rc_args)
        labs, tree = rc(dummy_data)
        
        return rc, labs, tree
    
    @pytest.fixture(autouse=str(os.environ.get("BUILD_TRUTH")).lower() in ['true', 't'])
    def update_truth(self, raccoon: Raccoon,hashed_name: str) -> None:
        """ Update ground truth. """

        rc, _, _ = raccoon

        shutil.copyfile(os.path.join(rc.out_path, "rc_results.pq"),
                        os.path.join(input_path, "ground_truth", "rc_results_{:s}.pq".format(hashed_name)))        
        shutil.copyfile(os.path.join(rc.out_path, "rc_tree.json"),
                        os.path.join(input_path, "ground_truth", "rc_tree_{:s}.json".format(hashed_name)))
        shutil.copyfile(os.path.join(rc.out_path, "params.csv"),
                        os.path.join(input_path, "ground_truth", "params_{:s}.csv".format(hashed_name)))

        
        
    def test_all_outputs(self, raccoon: Raccoon, hashed_name: str) -> None:
        """ Test all produced outputs. """
        
        truth_labels = pd.read_parquet(os.path.join(input_path, "ground_truth",
                                                "rc_results_{:s}.pq".format(hashed_name)))
        assert_frame_equal(raccoon[1], truth_labels)
        
        truth_tree = load_tree(os.path.join(input_path, "ground_truth",
                                                        "rc_tree_{:s}.json".format(hashed_name)))
        assert_tree_equal(raccoon[2], truth_tree)
        

    def test_all_written_outputs(self, raccoon: Raccoon, hashed_name: str) -> None:
        """ Test all outputs saved tp disk. """
        
        truth_labels = pd.read_parquet(os.path.join(input_path, "ground_truth",
                                                "rc_results_{:s}.pq".format(hashed_name)))
        loaded_labels = pd.read_parquet(os.path.join(raccoon[0].out_path, "rc_results.pq"))
        assert_frame_equal(loaded_labels, truth_labels)
        
        truth_tree = load_tree(os.path.join(input_path, "ground_truth",
                                                        "rc_tree_{:s}.json".format(hashed_name)))
        loaded_tree = load_tree(os.path.join(raccoon[0].out_path, "rc_tree.json"))
        assert_tree_equal(loaded_tree, truth_tree)
        
        truth_params = pd.read_csv(os.path.join(input_path, "ground_truth",
                                                "params_{:s}.csv".format(hashed_name)))
        loaded_params = pd.read_csv(os.path.join(raccoon[0].out_path, "params.csv"))
        assert_frame_equal(loaded_params, truth_params)
        