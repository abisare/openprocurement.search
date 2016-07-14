# -*- coding: utf-8 -*-
from datetime import datetime
import simplejson as json

from openprocurement.search.index import BaseIndex, logger


class PlanIndex(BaseIndex):
    """OpenProcurement Plans Index
    """
    __index_name__ = 'plans'

    def need_reindex(self):
        if not self.current_index:
            return True
        if self.index_age() > 120*3600:
            # TODO: make index_hours configurable
            dt = datetime.now()
            return dt.weekday() > 5 and dt.hour < 5
        return False

    def create_index(self, name):
        body = None
        try:
            tender_index = self.config['plan_index']
            logger.info("Load index settings from %s", tender_index)
            if tender_index:
                with open(tender_index) as f:
                    body = json.load(f)
        except (KeyError, ValueError) as e:
            logger.error("%s", str(e));
            pass
        self.engine.create_index(name, body=body)

    def finish_index(self, name):
        # TODO: create EDRPOU json
        return