import pandas as pd


class Out:
    def __init__(self):
        df = pd.DataFrame(columns=['DATA'])
        self.df = df

    def add_day(self, tools, day):
        for tool in tools:
            self.df.loc[str(tool) + ' (' + str(day) + ')'] = None

    def add_value(self, value, tool, day, i):
        self.df.loc[str(tool) + ' (' + str(day) + ')', i] = value

    def render(self):
        writer = pd.ExcelWriter('output.xlsx')
        self.df.to_excel(writer)
        writer.save()
        print('Saved')
