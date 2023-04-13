import numpy as np

class crop_agent:
    def __init__(self, gamma: float):

        # Discount Factor
        assert 0.0 < gamma <= 1.0
        self.gamma = gamma

        # Utility Function
        self.utility = []
