import time
import requests
from matplotlib.widgets import Button, Slider
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator
import matplotlib.ticker as ticker
from matplotlib import dates
from datetime import datetime
import matplotlib
import json

matplotlib.use('TkAgg')


class streamDetectionPlot(object):
    # Initial the figure parameters
    def __init__(self):
        # Turn the interactive mode on
        plt.ion()
        # initial the plot variable
        self.timestamp = []
        self.loadingValue = []
        self.highlightList = []
        self.highlightListTurnOn = True
        self.loadingValueRange = [0, 1]
        self.timestampRange = [0, 1]
        self.tableValue = [[0, 0]]
        self.timestamp1 = []
        self.loadingValue1 = []

        # initial the figure
        global fig
        fig = plt.figure(figsize=(18, 8), facecolor="white")
        fig.subplots_adjust(left=0.06, right=0.70)
        self.loadingGraph = fig.add_subplot(2, 1, 1)
        ##add_axes(rect,**kwargs) Meaning:##rect: left,bottom,width,height
        self.loadingTable = fig.add_axes([0.72, 0.1, 0.2, 0.8], frameon=False)

        # Add a scroll bar
        self.axcolor = 'lightgoldenrodyellow'
        self.axsb = fig.add_axes([0.06, 0.25, 0.65, 0.02], facecolor=self.axcolor)

        # Add the pause button
        self.pauseax = fig.add_axes([0.8, 0.25, 0.05, 0.02], facecolor=self.axcolor)

    # define the initial plot method
    def initPlot(self):
        # initial two lines
        self.line, = self.loadingGraph.plot_date(self.timestamp, self.loadingValue, fmt="-", color="red",
                                                 label="LoadingValue")
        self.loadingGraph.legend(loc="upper right", frameon=False)
        self.loadingGraph.grid(True)

        # Set the baseline of 5000, horizen use "axhline" while vertical uses "axvline"
        self.baseline = self.loadingGraph.axhline(5000, color='black', lw=1)

        # Add the "5000" to the y-axis label next to the line
        # trans = transforms.blended_transform_factory(
        #     self.loadingGraph.get_yticklabels()[0].get_transform(), self.loadingGraph.transData)
        # self.loadingGraph.text(0, 5000, "{:.0f}".format(5000), color="black", transform=trans, ha="right", va="center")

        # Set the title
        self.loadingGraph.set_title("Live update test")

        # set the x/y label of the first graph
        self.loadingGraph.set_xlabel("datetime")
        self.loadingGraph.set_ylabel("Loading Value")

        # axis format
        self.dateFormat = DateFormatter("%Y-%m-%d %H:%M:%S.%f")
        self.loadingGraph.xaxis.set_major_formatter(ticker.FuncFormatter(self.dateFormat))

        ##Configure the table
        self.loadingTableColumnName = ["timestamp", "Loading value"]
        self.loadingTable.set_xticks([])
        self.loadingTable.set_yticks([])

    # define the output method
    def DetectionPlot(self, timestamp, loadingValue):
        if not pause:
            # update the plot value of the graph
            self.timestamp.append(timestamp)
            self.loadingValue.append(loadingValue)

            # From string to datetime
            self.timestamp1 = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f") for d in self.timestamp]
            self.loadingValue = [float(i) for i in self.loadingValue]

            # pretty date names
            plt.gcf().autofmt_xdate()

            # update the x/y range
            self.timestampRange = [min(self.timestamp1),
                                   max(self.timestamp1) + dt.timedelta(minutes=0.1)]  # datetime style
            self.loadingValueRange = [min(self.loadingValue), max(self.loadingValue) + 0.01]

            # update the x/y axis limits
            self.loadingGraph.set_ylim(
                min(self.loadingValueRange), max(self.loadingValueRange))
            self.loadingGraph.set_xlim(
                self.timestampRange[1] - dt.timedelta(minutes=1), self.timestampRange[1])

            # Set the y-ticks if the variation is above 1000
            # https://stackoverflow.com/questions/39969217/ytick-overlapping-in-matplotlib
            # self.loadingValue1 = [min(self.loadingValue)]
            # for i in sorted(self.loadingValue[0:]):
            #     if i - self.loadingValue1[-1] > 1000:
            #         self.loadingValue1.append(i)

            # Set the ticks
            self.loadingGraph.xaxis.set_ticks(self.timestamp1)
            self.loadingGraph.yaxis.set_ticks(self.loadingValue1)

            # update the two lines
            self.line.set_xdata(self.timestamp1)
            self.line.set_ydata(self.loadingValue)

            # The x-data is being updated, but the plot ranges are not. When I put new data on the plot, it was all out of range. The solution was to add:
            self.loadingGraph.relim()
            self.loadingGraph.autoscale_view()

            # Rotate the x-array
            for tick in self.loadingGraph.get_xticklabels():
                tick.set_rotation(15)

            # Plot the value of y on the plot.
            # for xp, yp in zip(self.timestamp1[1:-1], self.loadingValue[1:-1]):
            #     label = "%s" % yp
            #     self.loadingGraph.text(xp, yp, label, fontsize=8, horizontalalignment='right', verticalalignment='bottom')

            # Clear the text first
            for txt in self.loadingGraph.texts:
                txt.set_visible(False)
            # Set the maximum and minimum value of y on the plot.
            self.max_y, self.min_y = max(self.loadingValue), min(self.loadingValue)
            self.max_x, self.min_x = self.timestamp1[self.loadingValue.index(self.max_y)], self.timestamp1[
                self.loadingValue.index(self.min_y)]
            self.maxlabel, self.minlabel = "Max: %s ms" % self.max_y, "Min: %s ms" % self.min_y
            self.loadingGraph.text(self.max_x, self.max_y, self.maxlabel, fontsize=8, horizontalalignment='right',
                                   verticalalignment='bottom')
            self.loadingGraph.text(self.min_x, self.min_y, self.minlabel, fontsize=8, horizontalalignment='right',
                                   verticalalignment='bottom')

            # update the highlight of the graph. The x will be 1 second varitation
            if float(loadingValue) >= 5000:
                self.highlightList = self.timestamp1
                self.highlightListTurnOn = True
            else:
                self.highlightListTurnOn = False
            if len(self.highlightList) != 0 and self.highlightListTurnOn is False:
                self.loadingGraph.axvspan(
                    self.highlightList[0] - dt.timedelta(seconds=1),
                    self.highlightList[-1] + dt.timedelta(seconds=1),
                    color='r',
                    edgecolor=None,
                    alpha=0.2
                )
                self.highlightList = []
                self.highlightListTurnOn = True

            # Update the table with the latest 5 entries
            self.loadingTableColumnName = ["timestamp", "Loading value"]
            self.loadingTable.text(0.15, 1, "LoadingTable", size=12)
            self.loadingTable = fig.add_axes([0.72, 0.1, 0.2, 0.8], frameon=False)
            self.loadingTable.set_xticks([])
            self.loadingTable.set_yticks([])
            self.tableValue.append([timestamp, loadingValue])

            if len(self.tableValue) >= 6: self.tableValue.pop(0)
            self.loadingTable.table(cellText=self.tableValue,
                                    colWidths=[0.5] * 2,
                                    colLabels=self.loadingTableColumnName,
                                    loc=1,
                                    cellLoc='center'
                                    )

            # Slider setting
            self.ssb = Slider(self.axsb, 'Scrollbar',
                              dates.date2num(self.timestampRange[0]),
                              dates.date2num(self.timestampRange[1]))
            self.ssb.on_changed(self.update)

        # Pause Button setting
        self.button = Button(self.pauseax, 'Pause', color='0.85', hovercolor='0.975')
        self.button.on_clicked(self.setpause)

        # plot pause 0.0001 second and then plot the next one.
        plt.pause(1)
        plt.draw()

    # Define the slider update function
    def update(self, val):
        self.sb = self.ssb.val
        self.xmin_time = dates.num2date(self.sb) - dt.timedelta(minutes=1)
        self.xmax_time = dates.num2date(self.sb)
        self.loadingGraph.axis(
            [self.xmin_time, self.xmax_time, min(self.loadingValueRange), max(self.loadingValueRange)])
        fig.canvas.draw_idle()

    # Define the pause button function
    def setpause(self, event):
        global pause
        pause = not pause
        print(pause)

    # Turn off the ion and show the plot.
    def close(self):
        plt.ioff()
        plt.show()


def Slippage_judge(url1,url2):
    flag = True
    while flag:
        try:
            result_oder = json.loads(requests.get(url1).text)['result']
            result_history = json.loads(requests.get(url2).text)['result']
            buy = result_oder['buy']
            sell = result_oder['sell']
            buy_price = float(buy[0]['Rate'])
            sell_price = float(sell[0]['Rate'])
            flag_bslp = True
            flag_ssip = True
            for i in result_history:
                if( i['OrderType'] == 'SELL') and (flag_ssip == True):
                    sell_ID = i['Id']
                    sell_slippage = sell_price - i['Price']
                    sell_time = i['TimeStamp']
                    price_s = i['Price']
                    flag_ssip = False
                if(i['OrderType'] == 'BUY') and (flag_bslp == True):
                    buy_slippage = i['Price'] - buy_price
                    buy_time = i['TimeStamp']
                    buy_ID = i['Id']
                    price_b = i['Price']
                    flag_bslp = False
                if(flag_bslp==False) and (flag_ssip==False):
                    break
            return_data = {'sell': {'sell_ID': sell_ID, 'sell_slippage': sell_slippage, 'sell_time': sell_time,'price_s':price_s},
            'buy': {'buy_ID': buy_ID, 'buy_slippage': buy_slippage, 'buy_time': buy_time,'price_b':price_b}}
            print(return_data)
            flag = False
            return return_data
        except:
            flag = True
            time.sleep(2)
            print('erro')


url1 = 'https://api.bittrex.com/api/v1.1/public/getorderbook?market=USD-BTC&type=both'
url2 = 'https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=USD-BTC'
clock_s = 0
clock_b = 0
li_s = []
li_b = []
graph = streamDetectionPlot()
graph.initPlot()
pause = False
while True:
    result = Slippage_judge(url1,url2)
    li_s.append(result['sell'])
    clock_s += 1
    li_b.append(result['buy'])
    clock_b += 1
    if(clock_s==3000):
        with open('sell_Slippage.txt','a') as s:
            s.write(json.dumps(li_s)+'\n')
            li_s = []
            clock_s = 0
    if(clock_b==3000):
        with open('buy_Slippage.txt','a') as b:
            b.write(json.dumps(li_b)+'\n')
            li_b = []
            clock_b = 0
    if('.' not in result['sell']['sell_time']):
        result['sell']['sell_time'] += '.00'
    graph.DetectionPlot(result['sell']['sell_time'].replace('T', ' '), str(format(float(result['sell']['sell_slippage']) / float(1), '.2f')))
    time.sleep(3)