import logging
from src.consts.logger import LOGGING_NAME
from src.models.stats.stats import Stats
from src.models.stats.session import Session
from src.models.stats.account import Account
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats
from src.models.stats.fortune import FortuneStats
from src.models.stats.satanic_zone import SatanicZoneStats

from src.models.events.base import BaseEvent
from src.models.events.gold import GoldEvent
from src.models.events.xp import XPEvent
from src.models.events.account import AccountEvent
from src.models.events.mail import MailEvent
from src.models.events.satanic_zone import SatanicZoneEvent


class GameStats:
    session = Session()
    account = Account()
    gold = GoldStats()
    xp = XPStats()
    fortune = FortuneStats()
    satanic_zone = SatanicZoneStats()
    season_mode = None
    logger = logging.getLogger(LOGGING_NAME)

    def process_event(self, event: BaseEvent):
        self.logger.log(logging.INFO,f"GameStats.process_event: {event}")
        if isinstance(event, GoldEvent):
            self.gold.update(currencyData=event.value, season_mode=self.season_mode)
        if isinstance(event, XPEvent):
            self.xp.add(event.value)
        if isinstance(event, AccountEvent):
            self.xp.update(total_xp=event.value.experience)
            self.season_mode = event.value.get_current_season_mode()
        if isinstance(event, MailEvent):
            self.session.update(has_mail=bool(event.value))
        if isinstance(event, SatanicZoneEvent):
            self.satanic_zone.update(event.value)

    def reset(self):
        logger = logging.getLogger(LOGGING_NAME)
        logger.info("Resetting all game stats...")
        
        self.session = Session()
        self.account = Account()
        self.gold = GoldStats()
        self.xp = XPStats()
        self.satanic_zone = SatanicZoneStats()
        self.season_mode = None
        
        logger.info("All stats have been reset")

    def update_hourly_stats(self):
        self.gold.update(
            gold_per_hour=self.session.calculate_value_per_hour(
                self.gold.total_gold_earned
            )
        )
        self.xp.update(
            xp_per_hour=self.session.calculate_value_per_hour(
                self.xp.total_xp_earned
            )
        )

    def get_stats(self):
        self.update_hourly_stats()
        return Stats(
            session=self.session,
            gold_stats=self.gold,
            xp_stats=self.xp,
            satanic_zone=self.satanic_zone
        )