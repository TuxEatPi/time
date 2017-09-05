import logging
import os
import sys
import time

import pytest
from click.testing import CliRunner

#from tuxeatpi_common.error import BrainError



class TestCli(object):

    @pytest.mark.order1
    def test_help(self, capsys):
        # --help
        runner = CliRunner()
        sys.argv = ['fakedaemon', '-I', 'intents/', '-w', 'tests/workdir/', '-D', 'bad_dialogs']
        with pytest.raises(SystemExit):
            from tuxeatpi_time.common import cli
