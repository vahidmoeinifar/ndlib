from ndlib.models.compartments.Compartment import Compartment, ConfigurationException

__author__ = 'Giulio Rossetti'
__license__ = "BSD-2-Clause"
__email__ = "giulio.rossetti@gmail.com"


class ConditionalComposition(Compartment):

    def __init__(self, condition, first_branch, second_branch, **kwargs):
        super(self.__class__, self).__init__(kwargs)
        if not isinstance(condition, Compartment) or not isinstance(first_branch, Compartment) \
                or not isinstance(second_branch, Compartment):
            raise ConfigurationException("Condition and branches must be of type Compartment.")

        self.condition = condition
        self.first_branch = first_branch
        self.second_branch = second_branch

    def execute(self, *args, **kwargs):
        test = self.condition.execute(*args, **kwargs)
        if test:
            return self.first_branch.execute(*args, **kwargs)
        else:
            return self.second_branch.execute(*args, **kwargs)
