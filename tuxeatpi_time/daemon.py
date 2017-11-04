"""Module defining Get time/day component daemon"""
import logging
import time

import locale
import datetime

from tuxeatpi_common.error import TuxEatPiError
from tuxeatpi_common.daemon import TepBaseDaemon
from tuxeatpi_common.wamp import is_wamp_topic, is_wamp_rpc


class Time(TepBaseDaemon):
    """Component giving time and day"""

    def __init__(self, name, workdir, intent_folder, dialog_folder, logging_level=logging.INFO):
        TepBaseDaemon.__init__(self, name, workdir, intent_folder, dialog_folder, logging_level)

    def main_loop(self):
        time.sleep(1)

    def set_config(self, config):
        """Save the configuration and reload the daemon"""
        return True

    @is_wamp_rpc("time")
    @is_wamp_topic("time")
    def time_(self):
        """Get time"""
        # TODO add parameter
        self.logger.info("time.time called")
        # Get time format
        time_format = locale.nl_langinfo(locale.T_FMT)
        now = datetime.datetime.now()
        now_fmt = now.strftime(time_format)
        # Get dialog
        dialog = self.get_dialog("time", time=now_fmt, hour=now.hour,
                                 minute=now.minute, second=now.second)
        # Say answer
        self.call("speech.say", text=dialog)

    @is_wamp_rpc("day")
    @is_wamp_topic("day")
    def day(self):
        """Get day"""
        self.logger.info("time.day called")
        # Get time format
        day_format = locale.nl_langinfo(locale.D_FMT)
        today_fmt = datetime.datetime.now().strftime(day_format)
        # Get dialog
        dialog = self.get_dialog("day", day=today_fmt)
        # Say answer
        self.call("speech.say", text=dialog)

    @is_wamp_rpc("help")
    def help_(self):
        """Help for time component"""
        pass


class TimeError(TuxEatPiError):
    """Base class for hotword exceptions"""
    pass
