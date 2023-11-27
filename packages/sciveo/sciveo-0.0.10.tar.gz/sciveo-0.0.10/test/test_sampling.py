#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2023
#

import unittest

from sciveo.common.sampling import RandomSampler


class TestSampling(unittest.TestCase):
  def test_random_1(self):
    config = {
        "booster": {
            "values": ["gbtree", "gblinear"]
        },
        "booster2": ["gbtree", "gblinear"],
        "learning_rate": {
          "min": 0.001,
          "max": 1.0
        },
        "gamma": {
          "min": 0.001,
          "max": 1.0
        },
        "max_depth": {
            "values": [3, 5, 7]
        },
        "min_child_weight": {
          "min": 1,
          "max": 150
        },
        "early_stopping_rounds": {
          "values" : [10, 20, 30, 40]
        },
    }

    sampler = RandomSampler(config, n_samples=10)
    self.assertTrue(len(sampler.samples) == 10)

  def test_config_fields(self):
    config = {
        "C1": {
          "values": ["gbtree", "gblinear"]
        },
        "C2": ["gbtree", "gblinear"],
        "C3": {
          "min": 0.001, "max": 1.0
        },
        "C4": {
          "values" : [10, 20, 30, 40]
        },
        "C5": 1.23,
        "C6": {
          "min": 1, "max": 10
        },
        "C7": (1.0, 2.2),
        "C8": (1, 10)
    }

    sampler = RandomSampler(config, n_samples=3)
    c = sampler()

    self.assertTrue(c("C1") in config["C1"]["values"])
    self.assertTrue(c("C2") in config["C2"])
    self.assertTrue(c("C4") in config["C4"]["values"])
    self.assertTrue(config["C3"]["min"] <= c("C3") and  c("C3") <= config["C3"]["max"])
    self.assertTrue(c("C5") == config["C5"])

    self.assertTrue(isinstance(c("C3"), float))
    self.assertTrue(isinstance(c("C6"), int))

    self.assertTrue(config["C7"][0] <= c("C7") and c("C7") <= config["C7"][1])
    self.assertTrue(isinstance(c("C7"), float))
    self.assertTrue(config["C8"][0] <= c("C8") and c("C8") <= config["C8"][1])
    self.assertTrue(isinstance(c("C8"), int))
