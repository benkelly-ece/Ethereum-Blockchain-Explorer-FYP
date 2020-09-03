'''
Author: Ben Kelly
'''
from csv import writer
import csv
import os
import etherscan
from web3 import Web3
from datetime import date
import plotly.graph_objects as go
import plotly as py
py.offline.init_notebook_mode(connected=True)
import pandas as pd
import datetime

'''
Gets Eth price and adds it to the EtherPrice CSV
'''
#for etherscan API
es = etherscan.Client(
    api_key='XHT1QMF1HM8QM1JQJA68WNPTJF2WP1JM84',
    cache_expire_after=5,
)

eth_price = es.get_eth_price()
eth_price_str = str(eth_price['ethusd'])

today = date.today()
day = today.strftime("%m/%d/%y")
row_contents = str(day+','+'-'+','+eth_price_str)
with open('EtherPrice.csv','a') as fd:
    fd.write('\n'+row_contents)

print('Updated ETH Value for today')


'''
Takes the last 30 rows from full EtherPrice CSV
Places them into their own CSV files to be used to
create a graph of the Ether value last 30 days
'''
def get_last_n_lines(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)
 
        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
 
    # return the reversed list
    return list(reversed(list_of_lines))


last_lines = get_last_n_lines("EtherPrice.csv", 30)

with open("EtherPrice_30days.csv", "w") as output:
    output.write('"Date(UTC)","UnixTimeStamp","Value"\n')
    for line in last_lines:
        output.write(line)
        
print('Created 30 day ETH value CSV')

'''
This section generates the graph
'''
df = pd.read_csv('D:\EtherPrice_30days.csv')


fig = go.Figure([go.Scatter(x=df['Date(UTC)'], y=df['Value'])])

fig.update_layout(
    margin=dict(l=5, r=5, t=40, b=0),
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 10
        ),
    yaxis_tickformat = '$',
    title='ETH value 30 day history'
)
fig.write_image('eth_price_chart_30days.png', width=565, height=325)
py.offline.plot(fig, filename='eth_price_chart_30days.html')
fig.show()
###############################

df2 = pd.read_csv('D:\EtherPrice.csv')


fig2 = go.Figure([go.Scatter(x=df2['Date(UTC)'], y=df2['Value'])])

fig2.update_layout(
    margin=dict(l=5, r=5, t=40, b=0),
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 100
        ),
    yaxis_tickformat = '$',
    xaxis_tickformat = '%d %B (%a)<br>%Y',
    title='ETH value history'
)
py.offline.plot(fig2, filename='eth_price_chart_alltime.html')


