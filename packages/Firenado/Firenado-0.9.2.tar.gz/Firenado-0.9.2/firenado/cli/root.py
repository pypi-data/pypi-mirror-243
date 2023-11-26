import click
import firenado.conf
import logging
import os
import taskio
from taskio import core
import sys


@taskio.root(root="firenado", taskio_conf=firenado.conf.taskio)
def firenado_cli(ctx):
    pass
