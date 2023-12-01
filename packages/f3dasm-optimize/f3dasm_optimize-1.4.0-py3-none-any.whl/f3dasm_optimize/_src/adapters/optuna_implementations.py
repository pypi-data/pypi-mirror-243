#                                                                       Modules
# =============================================================================

from typing import Dict

# Third party
import optuna

# Local
from .._protocol import DataGenerator, Domain
from ..optimizer import Optimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class OptunaOptimizer(Optimizer):
    def _construct_model(self, data_generator: DataGenerator):

        for i in range(len(self.data)):
            experiment_sample = self.data.get_experiment_sample(i)
            self.algorithm.add_trial(
                optuna.trial.create_trial(
                    params=experiment_sample.input_data,
                    distributions=domain_to_optuna_distributions(self.domain),
                    value=experiment_sample.to_numpy()[1],
                )
            )

    def _create_trial(self) -> Dict:
        optuna_dict = {}
        for name, parameter in self.domain.items():
            if parameter._type == 'float':
                optuna_dict[name] = self.trial.suggest_float(
                    name=name,
                    low=parameter.lower_bound,
                    high=parameter.upper_bound, log=parameter.log)
            elif parameter._type == 'int':
                optuna_dict[name] = self.trial.suggest_int(
                    name=name,
                    low=parameter.lower_bound,
                    high=parameter.upper_bound, step=parameter.step)
            elif parameter._type == 'category':
                optuna_dict[name] = self.trial.suggest_categorical(
                    name=name,
                    choices=parameter.categories)
            elif parameter._type == 'object':
                optuna_dict[name] = self.trial.suggest_categorical(
                    name=name, choices=[parameter.value])

        return optuna_dict
        # return ExperimentSample(dict_input=optuna_dict,
        # dict_output = {}, jobnumber = 0)

    def update_step(self, data_generator: DataGenerator):
        self.trial = self.algorithm.ask()
        experiment_sample = data_generator._run(
            self._create_trial(), domain=self.domain)
        self.algorithm.tell(self.trial, experiment_sample.to_numpy()[1])
        return experiment_sample


def domain_to_optuna_distributions(domain: Domain):
    optuna_distributions = {}
    for name, parameter in domain.items():
        if parameter._type == 'float':
            optuna_distributions[
                name] = optuna.distributions.FloatDistribution(
                low=parameter.lower_bound,
                high=parameter.upper_bound, log=parameter.log)
        elif parameter._type == 'int':
            optuna_distributions[
                name] = optuna.distributions.IntDistribution(
                low=parameter.lower_bound,
                high=parameter.upper_bound, step=parameter.step)
        elif parameter._type == 'category':
            optuna_distributions[
                name] = optuna.distributions.CategoricalDistribution(
                parameter.categories)
        elif parameter._type == 'object':
            optuna_distributions[
                name] = optuna.distributions.CategoricalDistribution(
                choices=[parameter.value])
    return optuna_distributions
