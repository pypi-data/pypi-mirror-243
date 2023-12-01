#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass

# Third-party
from evosax import BIPOP_CMA_ES, CMA_ES, DE, PSO, SimAnneal

# Local
from .adapters.evosax_implementations import EvoSaxOptimizer
from .optimizer import OptimizerParameters

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


@dataclass
class CMAES_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxCMAES optimizer"""

    population: int = 30


class EvoSaxCMAES(EvoSaxOptimizer):
    hyperparameters: CMAES_Parameters = CMAES_Parameters()
    evosax_algorithm = CMA_ES

# =============================================================================


@dataclass
class PSO_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxPSO optimizer"""

    population: int = 30


class EvoSaxPSO(EvoSaxOptimizer):
    hyperparameters: PSO_Parameters = PSO_Parameters()
    evosax_algorithm = PSO

# =============================================================================


@dataclass
class SimAnneal_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxSimAnneal optimizer"""

    population: int = 30


class EvoSaxSimAnneal(EvoSaxOptimizer):
    hyperparameters: SimAnneal_Parameters = SimAnneal_Parameters()
    evosax_algorithm = SimAnneal

# =============================================================================


@dataclass
class DE_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxDE optimizer"""

    population: int = 30


class EvoSaxDE(EvoSaxOptimizer):
    hyperparameters: DE_Parameters = DE_Parameters()
    evosax_algorithm = DE

# =============================================================================


@dataclass
class BIPOPCMAES_Parameters(OptimizerParameters):
    """Hyperparameters for EvoSaxBIPOP_CMAES optimizer"""

    population: int = 30


class EvoSaxBIPOPCMAES(EvoSaxOptimizer):
    hyperparameters: BIPOPCMAES_Parameters = BIPOPCMAES_Parameters()
    evosax_algorithm = BIPOP_CMA_ES
