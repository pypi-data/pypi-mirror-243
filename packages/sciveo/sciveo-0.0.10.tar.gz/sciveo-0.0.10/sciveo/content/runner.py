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
from sciveo.common.sampling import RandomSampler, GridSampler
from sciveo.content.project import RemoteProject, LocalProject


class ProjectRunner:
  current = None

  def __init__(self, project, function, remote=True, configuration={}, count=10, sampler="random"):
    self.project_name = project
    self.function = function
    self.count = count

    if sampler == "random":
      self.configuration_sampler = RandomSampler(configuration, count)
    elif sampler == "grid":
      self.configuration_sampler = GridSampler(configuration)
    else:
      self.configuration_sampler = RandomSampler(configuration, 10)

    if remote:
      self.project = RemoteProject(self.project_name)
    else:
      self.project = LocalProject(self.project_name)

  def run(self):
    for i in range(self.count):
      self.project.config = self.configuration_sampler()
      self.project.config.set_name(f"[{self.project.list_content_size + i + 1}]")
      debug(type(self).__name__, "run", i, self.project.config)
      self.function()
