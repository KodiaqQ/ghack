import pandas as pd
from Data import Data
import math


class Tool:
    def __init__(self, id):
        self.id = id
        self.time_left = 16
        self.debt = 0
        self.debt_all = 0
        self.details = Data().get_current_details()
        self.detail_t = 0
        self.detail_id = 0

    def add_detail(self, day, id):
        detail = self.details[str(id)]

        if self.time_left == 0:
            return 'n_added', 0
        if self.time_left < detail['total']:
            diff = detail['total'] - self.time_left
            self.debt_all = detail['batch']
            self.debt = detail['batch'] - math.floor(diff / detail['time'])
            self.time_left = 0
            self.detail_t = detail['time']
            self.detail_id = id
            print(
                'Detail ' + str(id)
                + ' is added at ' + str(day)
                + ' to tool - ' + str(self.id)
                + ' as debt - ' + str(self.debt))
            return 'debt', self.debt

        self.time_left -= detail['total']
        self.debt = 0

        print(
            'Detail ' + str(id)
            + ' is added at ' + str(pd.to_datetime(day))
            + ' to tool - ' + str(self.id)
            + ' left ' + str(self.time_left) + ' hours')
        return 'added', 16 - self.time_left

    def recount_day(self):
        self.time_left = 16
        if self.debt > 0:
            old = self.debt_all
            time = self.debt * self.detail_t
            self.time_left = self.time_left - time
            self.debt = 0
            self.debt_all = 0
            self.detail_t = 0

            return self.detail_id, old
        return None, None
