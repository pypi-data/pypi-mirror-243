import os
import unittest.util

from manageprojects.utilities.log_utils import log_config


# Hacky way to expand the failed test output:
unittest.util._MAX_LENGTH = os.environ.get('UNITTEST_MAX_LENGTH', 300)


log_config(
    format='%(levelname)s %(name)s.%(funcName)s %(lineno)d | %(message)s',
    log_in_file=False,
    raise_log_output=True,
)
