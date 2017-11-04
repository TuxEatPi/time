import os
import json
import time
import threading

import pytest
from wampy.peers import Client

from tuxeatpi_common.cli import main_cli, set_daemon_class
from tuxeatpi_time.daemon import Time
from tuxeatpi_common.message import Message


class FakeWampClient(Client):

    def fake_say(self, text):
        return


class TestTime(object):

    @classmethod
    def setup_class(self):
        workdir = "tests/workdir"
        intents = "intents"
        dialogs = "dialogs"
        self.time_daemon = Time('time_test', workdir, intents, dialogs)
        self.time_daemon.settings.language = "en_US"
        self.message = None


        def speech_say(text):
            self.message = text

        self.wamp_client = Client(realm="tuxeatpi")
        self.wamp_client.start()

        self.wamp_client.session._register_procedure("speech.say")
        setattr(self.wamp_client, "speech.say", speech_say)

    @classmethod
    def teardown_class(self):
        self.message = None
        self.time_daemon.settings.delete("/config/global")
        self.time_daemon.settings.delete("/config/time_test")
        self.time_daemon.settings.delete()
        self.time_daemon.registry.clear()
        try:  # CircleCI specific
            self.time_daemon.shutdown()
        except AttributeError:
            pass

    @pytest.mark.order1
    def test_time(self, capsys):
        t = threading.Thread(target=self.time_daemon.start)
        t = t.start()

        time.sleep(1)
        global_config = {"language": "en_US",
                         "nlu_engine": "fake_nlu",
                         }
        self.time_daemon.settings.save(global_config, "global")
        config = {}
        self.time_daemon.settings.save(config)
        self.time_daemon.set_config(config)

        self.time_daemon.time_()
        time.sleep(1)
        assert self.message is not None
        time.sleep(1)
        self.time_daemon.day()
        assert self.message is not None
