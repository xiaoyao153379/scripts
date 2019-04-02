This is a script that crawls real-time trading slippages.

The slip point calculation formula is:
Buy slippage = transaction price - the highest price of the pending order
Sell slippage = lowest price of market pending orders - transaction price

The information that is crawled mainly includes the ID of the transaction, the time of the transaction, the price of the bitcoin at the time, and the price of the slippage of the buy and sell.

This script is available in two versions. One is just to crawl the information, the other is to draw the information in real time through the python matlablib library to draw the chart.

If your computer is poorly configured, you can first crawl the data and then plot the analysis. Because I used my mac book pro to process this data, I think my computer configuration is not good enough.