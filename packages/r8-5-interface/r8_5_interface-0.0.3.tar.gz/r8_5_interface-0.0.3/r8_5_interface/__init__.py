# flake8: noqa

import pkg_resources


__version__ = pkg_resources.get_distribution("r8_5_interface").version


from r8_5_interface.r8_5 import R85
try:
    from r8_5_interface.interface import R85ROSRobotInterface
except ImportError:
    pass
