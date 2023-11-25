import copy
import collections
import numpy as np
import pandas as pd
from numpy.linalg import norm
from scipy.sparse import csgraph, issparse
from sklearn.metrics import pairwise_distances
                
class NotFittedError(ValueError, AttributeError):
    """Exception class to raise if estimator is used before fitting.
    """
        

def process_mst(min_spanning_tree):
    """
    Builds a single-linkage tree (SLT) from the provided minimum spanning tree
    (MST). The MST is first sorted then processed by a custom Cython routine.

    Parameters
    ----------
    min_spanning_tree : ndarray of shape (n_samples - 1,), dtype=MST_edge_dtype
        The MST representation of the mutual-reachability graph. The MST is
        represented as a collection of edges.

    Returns
    -------
    single_linkage : ndarray of shape (n_samples - 1,), dtype=HIERARCHY_dtype
        The single-linkage tree tree (dendrogram) built from the MST.
    """
    from .compute_tree import make_single_linkage
    # Sort edges of the min_spanning_tree by weight
    row_order = np.argsort(min_spanning_tree["distance"])
    min_spanning_tree = min_spanning_tree[row_order]
    # Convert edge list into standard hierarchical clustering format
    return make_single_linkage(min_spanning_tree)




def build_mst(mutual_reachability, min_samples):
    """
    Builds a minimum spanning tree (MST) from the provided mutual-reachability
    values. This function dispatches to a custom Cython implementation for
    dense arrays, and `scipy.sparse.csgraph.minimum_spanning_tree` for sparse
    arrays/matrices.

    Parameters
    ----------
    mututal_reachability_graph: {ndarray, sparse matrix} of shape \
            (n_samples, n_samples)
        Weighted adjacency matrix of the mutual reachability graph.

    min_samples : int, default=None
        The number of samples in a neighborhood for a point
        to be considered as a core point. This includes the point itself.

    Returns
    -------
    mst : ndarray of shape (n_samples - 1,), dtype=MST_edge_dtype
        The MST representation of the mutual-reachability graph. The MST is
        represented as a collection of edges.
    """
    from .compute_tree import mst_from_mutual_reachability, MST_edge_dtype
    
    if not issparse(mutual_reachability):
        return mst_from_mutual_reachability(mutual_reachability)

    # Check connected component on mutual reachability
    # If more than one component, it means that even if the distance matrix X
    # has one component, there exists with less than `min_samples` neighbors
    if (
        csgraph.connected_components(
            mutual_reachability, directed=False, return_labels=False
        )
        > 1
    ):
        raise ValueError(
            f"There exists points with fewer than {min_samples} neighbors. Ensure"
            " your distance matrix has non-zero values for at least"
            f" `min_sample`={min_samples} neighbors for each points (i.e. K-nn"
            " graph), or specify a `max_distance` in `metric_params` to use when"
            " distances are missing."
        )

    # Compute the minimum spanning tree for the sparse graph
    sparse_min_spanning_tree = csgraph.minimum_spanning_tree(mutual_reachability)
    rows, cols = sparse_min_spanning_tree.nonzero()
    mst = np.core.records.fromarrays(
        [rows, cols, sparse_min_spanning_tree.data],
        dtype=MST_edge_dtype,
    )
    return mst


def uniform_seed(X, num, sample_weight=None, metric='euclidean', random_state=42):

    """
    initialized the centroids with uniform initialization
    
    inputs:
        X - numpy array of data points having shape (n_samples, n_dim)
        num- number of clusters
    """
    np.random.seed(random_state)
    indices = np.random.choice(X.shape[0], size=num, replace=False, p=sample_weight)
    pair_dist = pairwise_distances(X, X[indices], metric=metric)
    labels = np.argmin(pair_dist, axis=1)
    nr_num = np.array([collections.Counter(labels)[i] for i in range(num)])
    return labels, np.vstack((indices, nr_num)).T


def kpp_seed(
    X, num, sample_weight=None, metric='euclidean', random_state=42, n_trials=None
):
    """k-means++ with arbitrary metrics

    Parameters
    ----------
    X : {ndarray, sparse matrix} of shape (n_samples, n_features)
        The data to pick seeds for.

    num : int
        The number of seeds to choose.

    sample_weight : ndarray of shape (n_samples,)
        The weights for each observation in `X`.

    metric : str or callable, default='euclidean'
        The metric to use when calculating distance between instances in a feature array. 
        If metric is a string, it must be one of the options allowed by scipy.spatial.distance.pdist 
        for its metric parameter, or a metric listed in pairwise.PAIRWISE_DISTANCE_FUNCTIONS. 
        If metric is “precomputed”, X is assumed to be a distance matrix. Alternatively, if metric 
        is a callable function, it is called on each pair of instances (rows) and the resulting value recorded.
        The callable should take two arrays from X as input and return a value indicating the distance
        between them.

    random_state : RandomState instance
        The generator used to initialize the centers.
        See :term:`Glossary <random_state>`.

    n_trials : int, default=None
        The number of seeding trials for each center (except the first),
        of which the one reducing inertia the most is greedily chosen.
        Set to None to make the number of trials depend logarithmically
        on the number of seeds (2+log(k)); this is the default.

    Returns
    -------
    centers : ndarray of shape (num, n_features)
        The initial centers for k-means.

    indices : ndarray of shape (num,)
        The index location of the chosen centers in the data array X. For a
        given index and center, X[index] = center.
    """
    
    if sample_weight is None:
        sample_weight = np.ones(X.shape[0], dtype=float)
        
    random_state = np.random.RandomState(random_state)
    n_samples, n_features = X.shape

    centers = np.empty((num, n_features), dtype=X.dtype)

    if n_trials is None:
        n_trials = 2 + int(np.log(num))

    center_id = random_state.choice(n_samples, p=sample_weight / sample_weight.sum())
    indices = np.full(num, -1, dtype=int)
    if issparse(X):
        centers[0] = X[center_id].toarray()
    else:
        centers[0] = X[center_id]
    indices[0] = center_id

    closest_dist_sq = pairwise_distances(centers[0, np.newaxis], X, metric=metric)
    current_pot = closest_dist_sq @ sample_weight

    for c in range(1, num):
       
        rand_vals = random_state.uniform(size=n_trials) * current_pot
        candidate_ids = np.searchsorted(
            np.cumsum(sample_weight * closest_dist_sq, dtype=np.float64), rand_vals
        )
        
        np.clip(candidate_ids, None, closest_dist_sq.size - 1, out=candidate_ids)

        distance_to_candidates = pairwise_distances(X[candidate_ids], X, metric=metric)

        np.minimum(closest_dist_sq, distance_to_candidates, out=distance_to_candidates)
        candidates_pot = distance_to_candidates @ sample_weight.reshape(-1, 1)

   
        best_candidate = np.argmin(candidates_pot)
        current_pot = candidates_pot[best_candidate]
        closest_dist_sq = distance_to_candidates[best_candidate]
        best_candidate = candidate_ids[best_candidate]

        if issparse(X):
            centers[c] = X[best_candidate].toarray()
        else:
            centers[c] = X[best_candidate]
        indices[c] = best_candidate
    
    pair_dist = pairwise_distances(X, centers, metric=metric)
    labels = np.argmin(pair_dist, axis=1)
    nr_num = np.array([collections.Counter(labels)[i] for i in range(num)])
    return labels, np.vstack((indices, nr_num)).T


"""


    def pairwise_dist_compute2(self, X, nr_grp):
        nr_grp = - np.log(1/nr_grp)
        pairD = self.pairwise_distances(X)
        return pairD * nr_grp + (pairD.T * nr_grp).T
    
    def pairwise_dist_compute3(self, X, nr_grp):
        pairD = self.pairwise_distances(X)
        D = np.ones(pairD.shape)
        return np.log(D / nr_grp + (D / nr_grp).T) + np.log(pairD)
    
    def pairwise_dist_compute4(self, X, nr_grp):
        pairD = self.pairwise_distances(X)
        return np.log(pairD / nr_grp + (pairD.T / nr_grp).T)
    
    def pairwise_dist_compute5(self, X, nr_grp):
        pairD = self.pairwise_distances(X)
        return pairD / nr_grp + (pairD.T / nr_grp).T
    
    def pairwise_dist_compute6(self, X, nr_grp):
        pairD = self.pairwise_distances(X)
        D = np.ones(pairD.shape)
        return -np.log(D / nr_grp + (D / nr_grp).T) * pairD
"""


class AEOM:
    """AEOM: Fast and explainable clustering based on sorting.
    
    The main parameters are ``eps`` and ``minPts``.
    
    Parameters
    ----------
    sorting : str, {'pca', 'norm-mean', 'norm-orthant', None}，default='pca'
        Sorting method used for the aggregation phase.
        
        - 'pca': sort data points by their first principal component
        
        - 'norm-mean': shift data to have zero mean and then sort by 2-norm values
        
        - 'norm-orthant': shift data to positive orthant and then sort by 2-norm values
        
        - None: aggregate the raw data without any sorting

        
    eps : float, default=0.5
        Tolerance to control the aggregation. If the distance between a group center 
        and an object is less than or equal to the tolerance, the object will be allocated 
        to the group which the group center belongs to. For details, we refer to [1].

    minPts : int, default=1
        Clusters with fewer than minPts points are classified as abnormal clusters.  
        The data points in an abnormal cluster will be redistributed to the nearest normal cluster. 
        When set to 1, no redistribution is performed. 

    norm : boolean, default=True
        If normalize the data associated with the sorting, default as True. 
        
    mergeScale : float
        Design for distance-clustering, when distance between the two group centers 
        associated with two distinct groups smaller than mergeScale*eps, then the two groups merge.

    post_alloc : boolean, default=True
        If allocate the outliers to the closest groups, hence the corresponding clusters. 
        If False, all outliers will be labeled as -1.

    memory : boolean, default=True
        If Cython memoryviews is disable, a fast algorithm with less efficient memory 
          consumption is triggered since precomputation for aggregation is used. 
        Setting it True will use a memory efficient computing.  
        If Cython memoryviews is effective, this parameter can be ignored. 
    
    verbose : boolean or int, default=1
        Whether to print the logs or not.
 
              
    Attributes
    ----------
    groups_ : numpy.ndarray
        Groups labels of aggregation.
    
    corelist_ : numpy.ndarray
        List of group centers formed in the aggregation.
        
    labels_ : numpy.ndarray
        Clustering class labels for data objects 

    clusterSizes_ : array
        The cardinality of each cluster.

    groupCenters_ : array
        The indices for starting point corresponding to original data order.

    
    Methods
    ----------
    fit(data):
        Cluster data while the parameters of the model will be saved. The labels can be extracted by calling ``self.labels_``.
        
    fit_transform(data):
        Cluster data and return labels. The labels can also be extracted by calling ``self.labels_``.
        
    predict(data):
        After clustering the in-sample data, predict the out-sample data.
        Data will be allocated to the clusters with the nearest starting point in the stage of aggregation. Default values.

    gcIndices(ids):
        Return the group center (i.e., starting point) location in the data.
        

    References
    ----------
    [1] X. Chen and S. Güttel. Fast and explainable sorted based clustering, 2022
    """
        
    def __init__(self, k=10, eps=0.5, minPts=2, method='default', sorting="pca", metric='euclidean', 
                 sample_weight=None, n_trials=None, post_alloc=True, memory=True, random_state=42, verbose=1): 

        self.verbose = verbose
        self.k = k
        self.eps = eps
        self.minPts = minPts
        self.method = method

        self.sorting = sorting
        self.metric = metric
        self.sample_weight = sample_weight
        self.n_trials = n_trials

        self.post_alloc = post_alloc
        self.random_state = random_state
        
        self.sp_info = None
        self.connected_paths = None
        
        self._gcIndices = np.frompyfunc(self.gc2ind, 1, 1)
                     
        if self.verbose:
            print(self)
        
        self.index_data = None
        self.memory = memory

        from .aggregate import aggregate
        from .aggregate import aggregate as precompute_aggregate, precompute_aggregate_pca
        from .merge import mutual_reachability_graph
        from .compute_tree import tree_to_labels
        self.pairwise_distances = pairwise_distances
        self.tree_to_labels = tree_to_labels

        self.mu_tual_reachability_graph = mutual_reachability_graph

        if not self.memory:
            if sorting == 'pca':
                self._aggregate = precompute_aggregate_pca
            else:
                self._aggregate = precompute_aggregate
            
        else:
            self._aggregate = aggregate
        


    def fit(self, data):
        """ 
        Cluster the data and return the associated cluster labels. 
        
        Parameters
        ----------
        data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)
        
            
        """
        if isinstance(data, pd.core.frame.DataFrame):
            self.index_data = data.index
            
        if not isinstance(data, np.ndarray):
            data = np.array(data)
            if len(data.shape) == 1:
                data = data.reshape(-1,1)
                
        if data.dtype !=  'float64':
            data = data.astype('float64')
            
        if self.sorting == "norm-mean":
            self.mu_ = data.mean(axis=0)
            self.data = data - self.mu_
            self.dataScale_ = self.data.std()
            if self.dataScale_ == 0: # prevent zero-division
                self.dataScale_ = 1
            self.data = self.data / self.dataScale_
        
        elif self.sorting == "pca":
            self.mu_ = data.mean(axis=0)
            self.data = data - self.mu_ # mean center
            rds = norm(self.data, axis=1) # distance of each data point from 0
            self.dataScale_ = np.median(rds) # 50% of data points are within that eps
            if self.dataScale_ == 0: # prevent zero-division
                self.dataScale_ = 1
            self.data = self.data / self.dataScale_ # now 50% of data are in unit ball 
            
        elif self.sorting == "norm-orthant":
            self.mu_ = data.min(axis=0)
            self.data = data - self.mu_
            self.dataScale_ = self.data.std()
            if self.dataScale_ == 0: # prevent zero-division
                self.dataScale_ = 1
            self.data = self.data / self.dataScale_
            
        else:
            self.mu_, self.dataScale_ = 0, 1 # no normalization
            self.data = (data - self.mu_) / self.dataScale_
        
        # aggregation
        if self.method == 'pca':
            if not self.memory:
                self.groups_, self.corelist_, self.dist_nr, self.ind, self.data, self.half_nrm2 = self._aggregate(data=self.data,
                                                                                                        sorting=self.sorting, 
                                                                                                        tol=self.eps
                                                                                                    ) 
            else:
                self.groups_, self.corelist_, self.dist_nr, self.ind, self.data = self._aggregate(data=self.data,
                                                                                                    sorting=self.sorting, 
                                                                                                    tol=self.eps
                                                                                                ) 
                
            self.corelist_ = np.array(self.corelist_)
            self.groups_ = np.array(self.groups_)

        elif self.method == 'random':
            self.groups_, self.corelist_ = uniform_seed(self.data, self.k, sample_weight=self.sample_weight, metric=self.metric, random_state=self.random_state)
        
        else:
            self.groups_, self.corelist_ = kpp_seed(self.data, self.k, 
                                                        sample_weight=self.sample_weight, 
                                                        metric=self.metric, 
                                                        random_state=self.random_state, 
                                                        n_trials=self.n_trials
                                                    )



        self.labels_, self.probabilities_ = self.merging(
            data=self.data,
            agg_labels=self.groups_, 
            splist=self.corelist_,  
            minPts=self.minPts
        ) 

        return self


        
    def fit_transform(self, data):
        """ 
        Cluster the data and return the associated cluster labels. 
        
        Parameters
        ----------
        data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)
        
        Returns
        -------
        labels : numpy.ndarray
            Index of the cluster each sample belongs to.
            
        """
        
        return self.fit(data).labels_
        
        
        
    def predict(self, data, memory=False):
        """
        Allocate the data to their nearest clusters.
        
        - data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)

        - memory : bool, default=False
        
            - True: default, use precomputation is triggered to speedup the query

            - False: a memory efficient way to perform query 

        Returns
        -------
        labels : numpy.ndarray
            The predicted clustering labels.
        """
        
        if hasattr(self, 'labels_'):
            if not hasattr(self, 'label_change'):
                if not hasattr(self, 'inverse_ind'):
                    self.inverse_ind = np.argsort(self.ind)
                groups = np.asarray(self.groups_)    
                self.label_change = dict(zip(groups[self.inverse_ind], self.labels_)) 
        else:
            raise NotFittedError("Please use .fit() method first.")
            
        labels = list()
        data = self.normalization(np.asarray(data))
        indices = self.corelist_[:,0].astype(int)
        splist = data[indices]
        num_of_points = data.shape[0]
        
        if not memory:
            xxt = np.einsum('ij,ij->i', splist, splist)
            for i in range(num_of_points):
                splabel = np.argmin(euclid(xxt, splist, data[i]))
                labels.append(self.label_change[splabel])

        else:
            for i in range(num_of_points):
                splabel = np.argmin(np.linalg.norm(splist - data[i], axis=1, ord=2))
                labels.append(self.label_change[splabel])

        return labels
    
    
    
    def merging(self, data, agg_labels, splist, minPts, cluster_selection_method="eom", 
                                    allow_single_cluster=False, cluster_epsilon=0.0, max_cluster_size=None):
        """
        Merge groups after aggregation. 

        Parameters
        ----------
        data : numpy.ndarray
            The input that is array-like of shape (n_samples,).
        
        agg_labels: list
            Groups labels of aggregation.
        
        splist: numpy.ndarray
            List formed in the aggregation storing group centers.
        
        cluster_selection_method : string, optional (default 'eom')
            The method of selecting clusters. The default is the
            Excess of Mass algorithm specified by 'eom'. The alternate
            option is 'leaf'.

        allow_single_cluster : boolean, optional (default False)
            Whether to allow a single cluster to be selected by the
            Excess of Mass algorithm.

        cluster_epsilon: double, optional (default 0.0)
            A distance threshold for cluster splits.

        max_cluster_size: int, default=None
            The maximum size for clusters located by the EOM clusterer. Can
            be overridden by the cluster_selection_epsilon parameter in
            rare cases.


        Returns
        -------
        labels : numpy.ndarray 
            The clusters labels of the data

        probabilities : ndarray (n_samples,)
            The cluster membership strength of each group center.

        """

        spdata = data[splist[:,0]]
        distance_matrix = self.pairwise_dist_compute(spdata, splist[:, 1])

        mutual_reachability_ = self.mu_tual_reachability_graph(distance_matrix, min_samples=minPts, max_distance=1)
        min_spanning_tree = process_mst(build_mst(mutual_reachability=mutual_reachability_, min_samples=minPts))

        labels, probabilities = self.tree_to_labels(
                            single_linkage_tree=min_spanning_tree, 
                            min_cluster_size=minPts, 
                            cluster_selection_method=cluster_selection_method, 
                            allow_single_cluster=allow_single_cluster, 
                            cluster_selection_epsilon=cluster_epsilon, 
                            max_cluster_size=max_cluster_size
                        )

        if self.post_alloc and np.any(labels == -1) and np.any(labels > -1):
            outdist = self.pairwise_distances(spdata[labels == -1], spdata[labels > -1])
            outll = np.argmin(outdist, axis=1)
            labels[labels == -1] = labels[labels > -1][outll]

        if self.method == 'pca':
            ll = agg_labels[np.argsort(self.ind)]
            return labels[ll], probabilities
        else:
            return labels[agg_labels], probabilities



    def pairwise_dist_compute(self, X, nr_grp):
        pairD = self.pairwise_distances(X)
        return pairD / nr_grp + (pairD.T / nr_grp).T

    

    def normalization(self, data):
        """
        Normalize the data by the fitted model.
        """

        if hasattr(self, 'labels_'):
            return (data - self.mu_) / self.dataScale_ 
        else:
            raise NotFittedError("Please use .fit() method first.")
        


    @property
    def groupCenters_(self):
        if hasattr(self, 'corelist_'):
            return self._gcIndices(np.arange(self.corelist_.shape[0]))
        else:
            raise NotFittedError("Please use .fit() method first.")
            
    
    
    @property
    def clusterSizes_(self):
        if hasattr(self, 'corelist_'):
            counter = collections.Counter(self.labels_)
            return np.array(list(counter.values()))[np.argsort(list(counter.keys()))]
        else:
            raise NotFittedError("Please use .fit() method first.")

    
    
    def gcIndices(self, ids):
        return self._gcIndices(ids)


        
    def gc2ind(self, spid):
        return self.ind[self.corelist_[spid, 0]]


    
    def load_group_centers(self):
        """Load group centers."""
        
        if not hasattr(self, 'groups_'):
            raise NotFittedError("Please use .fit() method first.")
            
        if not hasattr(self, 'grp_centers'):
            self.grp_centers = calculate_cluster_centers(self.data, self.groups_)
            return self.grp_centers
        else:
            return self.grp_centers
        
        

    def load_cluster_centers(self):
        """Load cluster centers."""
            
        if not hasattr(self, 'labels_'):
            raise NotFittedError("Please use .fit() method first.")
            
        if not hasattr(self, 'centers'):
            self.centers = calculate_cluster_centers(self.data[self.inverse_ind], self.labels_)
            return self.centers
        else:
            return self.centers
        
        
    def calculate_group_centers(self, data, labels):
        """Compute data center for each label according to label sequence."""
        
        centers = list() 
        for c in set(labels):
            indc = [i for i in range(data.shape[0]) if labels[i] == c]
            indc = (labels==c)
            center = [-1, c] + np.mean(data[indc,:], axis=0).tolist()
            centers.append( center )
            
        return centers

    
    
    def outlier_filter(self, min_samples=None, min_samples_rate=0.1): # percent
        """Filter outliers in terms of ``min_samples`` or ``min_samples_rate``. """
        
        if min_samples == None:
            min_samples = min_samples_rate*sum(self.old_cluster_count.values())
            
        return [i[0] for i in self.old_cluster_count.items() if i[1] < min_samples]
    


    def reassign_labels(self, labels):
        """Renumber the labels to 0, 1, 2, 3, ..."""
        
        sorted_dict = sorted(self.old_cluster_count.items(), key=lambda x: x[1], reverse=True)

        clabels = copy.deepcopy(labels)
        for i in range(len(sorted_dict)):
            clabels[labels == sorted_dict[i][0]]  = i

        return clabels

    

    def pprint_format(self, items, truncate=True):
        """Format item value for clusters. """
        
        cluster_sizes = [str(value) for key, value in sorted(items.items(), key=lambda x: x[1], reverse=True)]
        
        if truncate:
            if len(cluster_sizes) > 20: 
                dotstr = ',...'
                cluster_sizes = cluster_sizes[:20]
            else: 
                dotstr = '.'
            
        print(" ", ",".join(cluster_sizes) + dotstr)
                
        return 
            

            
    def __repr__(self):
        _name = "CLASSIX(eps={0.eps!r}, minPts={0.minPts!r})".format(self)
        return _name 

    
    
    def __str__(self):
        _name = 'CLASSIX(eps={0.eps!r}, minPts={0.minPts!r})'.format(self)
        return _name
    
    
    
    @property
    def eps(self):
        return self._eps
    
    
    
    @eps.setter
    def eps(self, value):
        if not isinstance(value, float) and not isinstance(value,int):
            raise TypeError('Expected a float or int type')
        if value <= 0:
            raise ValueError(
                "Please feed an correct value (>0) for tolerance.")
 
        self._eps = value
    
    
        
    @property
    def sorting(self):
        return self._sorting
    
    
    
    @sorting.setter
    def sorting(self, value):
        if not isinstance(value, str) and not isinstance(value, type(None)):
            raise TypeError('Expected a string type')
        if value not in ['pca', 'norm-mean', 'norm-orthant'] and value != None:
            raise ValueError(
                "Please refer to an correct sorting way, namely 'pca', 'norm-mean' and 'norm-orthant'.")
        self._sorting = value


    
    @property
    def minPts(self):
        return self._minPts
    
    
    
    @minPts.setter
    def minPts(self, value):
        if isinstance(value, str):
            raise TypeError('Expected a float or int type.')
        
        if isinstance(value, bool):
            raise TypeError('Expected a float or int type.')
        
        if isinstance(value, dict):
            raise TypeError('Expected a float or int type.')
        
        if hasattr(value, "__len__"):
            raise TypeError('Expected a scalar.')
        
        if value < 0 or (0 < value & value < 1):
            raise ValueError('Noise_mergeScale must be 0 or greater than 1.')
        
        self._minPts = int(round(value))
    

    
def normalization(data, base):
    """Initial data preparation of CLASSIX."""
    if base == "norm-mean":
        _mu = data.mean(axis=0)
        ndata = data - _mu
        dataScale = ndata.std()
        ndata = ndata / dataScale

    elif base == "pca":
        _mu = data.mean(axis=0)
        ndata = data - _mu # mean center
        rds = norm(ndata, axis=1) # distance of each data point from 0
        dataScale = np.median(rds) # 50% of data points are within that eps
        ndata = ndata / dataScale # now 50% of data are in unit ball 

    elif base == "norm-orthant":
        _mu = data.min(axis=0)
        ndata = data - _mu
        dataScale = ndata.std()
        ndata = ndata / dataScale

    else:
        _mu, dataScale = 0, 1 # no normalization
        ndata = (data - _mu) / dataScale
    return ndata, (_mu, dataScale)



def calculate_cluster_centers(data, labels):
    """Calculate the mean centers of clusters from given data."""
    classes = np.unique(labels)
    centers = np.zeros((len(classes), data.shape[1]))
    for c in classes:
        centers[c] = np.mean(data[labels==c,:], axis=0)
    return centers



def euclid(xxt, X, v):
    return (xxt + np.inner(v,v).ravel() -2*X.dot(v)).astype(float)





