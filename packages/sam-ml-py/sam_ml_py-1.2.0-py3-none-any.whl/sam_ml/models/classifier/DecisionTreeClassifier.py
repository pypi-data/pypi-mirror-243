from ConfigSpace import Categorical, ConfigurationSpace, Float, Integer
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier

from ..main_classifier import Classifier


class DTC(Classifier):
    """ DecisionTreeClassifier Wrapper class """

    def __init__(
        self,
        model_name: str = "DecisionTreeClassifier",
        random_state: int = 42,
        **kwargs,
    ):
        """
        @param (important one):
            criterion: function to measure the quality of a split
            max_depth: Maximum number of levels in tree
            min_samples_split: Minimum number of samples required to split a node
            min_samples_leaf: Minimum number of samples required at each leaf node
            random_state: random_state for model
        """
        model_type = "DTC"
        model = DecisionTreeClassifier(
            random_state=random_state,
            **kwargs,
        )
        grid = ConfigurationSpace(
            seed=42,
            space={
            "criterion": Categorical("criterion", ["gini", "entropy"], default="gini"),
            "max_depth": Integer("max_depth", (1, 12), default=5),
            "min_samples_split": Integer("min_samples_split", (2, 10), default=2),
            "min_samples_leaf": Integer("min_samples_leaf", (1, 5), default=1),
            "min_weight_fraction_leaf": Float("min_weight_fraction_leaf", (0, 0.5), default=0),
            "max_features": Categorical("max_features", ["log2","sqrt", 1.0], default=1.0),
            "max_leaf_nodes": Integer("max_leaf_nodes", (10, 90), default=90),
            })
        super().__init__(model, model_name, model_type, grid)
    
    def plot_tree(self):
        return tree.plot_tree(self.model)
