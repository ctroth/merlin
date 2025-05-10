from abc import ABC, abstractmethod 
from typing import Dict, Any

#abc is a built in module in Python that provides tools for defining abstract base classes.
#it allows you to create classes that cannot be instantiated directly, and must be subclassed by other classes.
#@ is a decorator that is used to define abstract methods in a class.  an abstract method is a method that is declared but contains no implementation.
#subclasses of the abstract base class must provide an implementation for the abstract method in order to be instantiated.

class Check(ABC):
    """
    Abstract base for all Argus checks.
    Defines the contract: every check must implement run().
    """
    name: str = "base"

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the check and return:
          - name (str)
          - status ("OK","WARN","CRIT","UNKNOWN")
          - metrics (Dict[str, Any])
          - details (Optional[str])
        """

    def evaluate(self, metric_name: str, value: float) -> str:
        """
        Compare `value` against `self.config['thresholds'][self.name]` definitions.
        Returns status string.
        """
        thresholds = self.config.get('thresholds', {}).get(self.name, {})
        if value >= thresholds.get('crit', float('inf')):
            return "CRIT"
        if value >= thresholds.get('warn', float('inf')):
            return "WARN"
        return "OK"
