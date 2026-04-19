from src.models.stats.session import Session
from src.models.stats.gold import GoldStats
from src.models.stats.xp import XPStats
from src.models.stats.satanic_zone import SatanicZoneStats


class Stats:
    session: Session
    gold: GoldStats
    xp: XPStats
    satanic_zone: SatanicZoneStats

    def __init__(self, session=Session(), gold_stats=GoldStats(), xp_stats=XPStats(), satanic_zone=SatanicZoneStats()):
        self.session = session
        self.gold = gold_stats
        self.xp = xp_stats
        self.satanic_zone = satanic_zone