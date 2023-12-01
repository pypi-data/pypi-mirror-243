#                                                                       Modules
# =============================================================================

# Third party
import optuna

# Local
from .adapters.optuna_implementations import OptunaOptimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class TPESampler(OptunaOptimizer):
    def set_algorithm(self):
        self.algorithm = optuna.create_study(
            sampler=optuna.samplers.TPESampler(seed=self.seed))
