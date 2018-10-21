import pandas as pd


class Data:
    def __init__(self):
        self.plan = pd.read_excel('data/1_plan.xls').drop(columns=['CEH'])
        self.schedule = pd.read_excel('data/2_schedule.xls').drop(columns=['CEH'])
        self.timing = pd.read_excel('data/4_timing.xls').drop(columns=['CEH'])
        self.batch = pd.read_excel('data/5_batch.xls').drop(columns=['CEH'])
        self.tools = pd.read_excel('data/3_tools.xls').drop(columns=['CEH'])

    def get_plan(self):
        needle = self.make_unique()

        plan = self.plan
        plan['TOTAL'] = pd.Series(0)
        plan['TOOLS'] = pd.Series(0)
        plan['NEEDLE'] = pd.Series(0)
        plan = plan[plan['DET'].isin(needle)]

        return plan

    def add_total(self, plan):
        needle = self.make_unique()

        base_details = self.get_current_details()
        for index in needle:
            plan.loc[index, 'TOTAL'] = base_details[str(index)]['total']
            plan.loc[index, 'NEEDLE'] = base_details[str(index)]['time']
            plan.loc[index, 'TOOLS'] = len(base_details[str(index)]['tools'])

        return plan.dropna()

    def make_unique(self):
        plan_uniq = self.plan['DET'].unique()
        timing_uniq = self.timing['DET'].unique()
        batch_uniq = self.batch['DET'].unique()

        needle = set(plan_uniq) & set(timing_uniq)
        needle = set(needle) & set(batch_uniq)

        return needle

    def make_tools(self):
        tools = {}
        needle = self.make_unique()

        for i, row in self.timing.iterrows():
            index = int(row['DET'])
            if index in needle:
                if index not in tools:
                    tools[index] = []
                tools[index].append(int(row['INV_NOM']))

        return tools

    def get_current_details(self):
        base_details = {}

        timing_arr = self.timing.set_index('DET').to_dict()['TIME_IZG']
        batch_arr = self.batch.set_index('DET').to_dict()['PARTY']

        plan_count = self.plan[['DET', 'QUANT_DAY']].groupby('DET').agg('sum').to_dict()['QUANT_DAY']

        needle = self.make_unique()

        tools = self.make_tools()

        for index in needle:
            if index not in base_details:
                base_details[str(index)] = {}
            base_details[str(index)].update({
                'time': timing_arr[index],
                'batch': batch_arr[index],
                'plan': int(plan_count[index]),
                'tools': tools[index],
                'total': batch_arr[index] * timing_arr[index],
                'balance': 0,
                'need': 0
            })

        return base_details
