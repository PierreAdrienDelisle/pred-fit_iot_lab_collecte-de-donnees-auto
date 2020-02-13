# PRED 2019/2020 - Automatic sensor data collection over a smart building

## Group
- DA SILVA Samuele
- DELISLE Pierre-Adrien

## Project explanation

The aim of this project is an automatic data collection, in the range of a smart building. The smart building here, being the Lille FIT IoT lab site. The cards we use are M3 cards, which represent a majority of the hardware available
on this site.
The collected data is to be stored in a Time Series Database, which is designed for researchers to use.

In order to collect the data, several developments were necessary, and every part of the project is available here, on this GitHub.

These parts accomplish several actions, which are be quickly presented in this document. For more information, you can check the Wiki.

### Firmware:

In order to collect the data from the M3 cards, we need a firmware to run on them. You can find two examples of firmwares here that pretty much accomplish the same things:
- Start the cards, initiate the sensor drivers
- Begin data collection: Gather 5 light values / 5 pressure values
- Send the values over the serial link.


### Python script - Data Collector:

The central part of the project, which pretty much controls the whole data collection. This python script accomplishes several tasks, which are presented thouroughly in the sequence diagram. As a quick presentation, here is what is does:
- Gather info about the testbed status, especially: How many m3 cards are available in Lille   
- Submit an experience with a certain percentage of the available nodes, the needed firmware / monitoring profile.
- Start the serial aggregator
- Gather all the data from the nodes
- Compute them and push them in the TSDB

You can also run this script at any time you want using the following:

### CRON:

In order to make this gathering automatic, we use Crontab. You can find the scripts necessary to the automatic execution in the GitHub.
### TSDB:

The Time Series database in which is stored the data. You can find a database scheme that we advice in the GitHub.

In any case, you can find more information about the project of the different parts in the Wiki.
