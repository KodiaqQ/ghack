import pandas as pd
from tkinter import *
from Data import Data
from Tool import Tool
from Out import Out
from Interface import Interface
from datetime import datetime, timedelta

pd.set_option('display.max_rows', 500)


def start(event):
    main(plan_p=btn_plan,
         schedule_p=btn_schedule,
         timing_p=btn_timing,
         batch_p=btn_batch,
         tools_p=btn_tools)


def main(plan_p, schedule_p, timing_p, batch_p, tools_p):
    data = Data(plan_p, schedule_p, timing_p, batch_p, tools_p)
    details = data.get_current_details()

    tools = {}
    for i, row in data.tools.iterrows():
        tools[row['INV_NOM']] = Tool(row['INV_NOM'], plan_p, schedule_p, timing_p, batch_p, tools_p)

    plan = data.get_plan()

    dates = data.schedule.replace(0, None)
    dates = pd.to_datetime(dates.dropna()['DATA'])
    dates = dates.astype(str).values

    martix = Out()

    for day in dates:
        martix.add_day(tools, day)
        print('Start - ' + str(day) + '...')
        list_today = plan[plan['DATA'] == day]
        list_today = list_today.groupby('DET').agg('sum')

        list_today = data.add_total(list_today)
        list_today = list_today.sort_values(by=['TOOLS', 'TOTAL'], ascending=[True, True])
        list_today['VALUE'] = list_today['QUANT_DAY'] * list_today['NEEDLE']
        for i, detail in list_today.iterrows():
            details[str(i)]['need'] += detail['QUANT_DAY']
            if detail['QUANT_DAY'] <= details[str(i)]['balance']:
                details[str(i)]['balance'] -= detail['QUANT_DAY']
                continue
            det = details[str(i)]
            max = 0
            tid = 0
            for tool in det['tools']:
                if tools[tool].time_left == 0:
                    continue
                if tools[tool].time_left > max:
                    max = tools[tool].time_left
                    tid = tool
                else:
                    continue
                result, num = tools[tid].add_detail(day, i)

                if result == 'added':
                    # 'Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'
                    details[str(i)]['balance'] += details[str(i)]['plan'] - detail['QUANT_DAY']
                    timestamp = datetime.strptime(day + ' 08:00:00', '%Y-%m-%d %H:%M:%S') + timedelta(days=num / 24)
                    martix.add_value(timestamp.strftime('%H:%M'), tool, day, i)
                    continue
                elif result == 'n_added':
                    break
                else:
                    if num < detail['QUANT_DAY']:
                        details[str(i)]['balance'] = detail['QUANT_DAY']
                    else:
                        details[str(i)]['balance'] = num - detail['QUANT_DAY']
                    break
        for index in tools:
            id, debt = tools[index].recount_day()
            if id is not None:
                details[str(id)]['balance'] = debt

    martix.render()


tk = Interface()
btn_plan = tk.load_file('Загрузить план')
btn_schedule = tk.load_file('Загрузить расписание')
btn_tools = tk.load_file('Загрузить станки')
btn_timing = tk.load_file('Загрузить время обработки')
btn_batch = tk.load_file('Загрузить норму по деталям')
btn = Button(tk.root, text='Начать расчёт',
             width=20, height=2,
             bg="white", fg="black")
btn.bind('<Button>', start)
btn.pack()
tk.root.mainloop()
