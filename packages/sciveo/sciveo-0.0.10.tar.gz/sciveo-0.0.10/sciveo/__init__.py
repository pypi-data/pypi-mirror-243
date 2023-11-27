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

import os

from sciveo.common.tools.logger import *
from sciveo.content.runner import ProjectRunner
from sciveo.content.dataset import Dataset


# New Experiment
def open():
  if ProjectRunner.current is not None:
    return ProjectRunner.current.project
  else:
    error("there is no started project")

def start(project, function, remote=True, configuration={}, count=10, sampler="random"):
  debug(f"start remote[{remote}] count[{count}] sampler[{sampler}]", configuration)

  ProjectRunner.current = ProjectRunner(project=project, function=function, remote=remote, configuration=configuration, count=count, sampler=sampler)
  ProjectRunner.current.run()

# Dataset info
def dataset(info={}):
  return Dataset.get(info)