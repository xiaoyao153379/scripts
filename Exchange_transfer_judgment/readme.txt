This is a monitoring script for the exchange wallet address transfer.

The main function of this script is to monitor the number of digital coins in the exchange wallet. And the example of a digital coin in this script is xrp(ripple).

Idea:
If someone makes a large transfer, it can be monitored in time.

You can set two monitored thresholds, here are two cases.

First, it is possible that a large trader trades in a one-time large transfer. In this case, I use the amount of the last second of the exchange wallet to compare with the amount of the next second. The reduced value is greater than the threshold I set, and the script will send me an email to remind me.

Second, it is possible that a large trader is trading a small number of times. For this situation, I am using a threshold that initially sets a comparison. This threshold does not change over time, but if the number of digital coins on the exchange accumulates to a certain number and the value of the subtraction is greater than the threshold I set, the script will send me an email to remind me.

it's not finished yet. This script can also be expanded. As you can see, the script I wrote doesn't just collect information about an exchange, but two. Only the parameter url passed in the function is different. Therefore, on this basis, it is entirely possible to add the addresses of all popular exchanges on the market to this script, and count the number of digital coins transferred from the user's private wallet to the exchange, so as to conduct a deeper analysis based on this information.