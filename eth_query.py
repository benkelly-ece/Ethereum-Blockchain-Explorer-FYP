'''
Author: Ben Kelly
'''
import sqlite3
import math
import etherscan
import threading
import time
import datetime
import webbrowser
import re
import statistics
from web3 import Web3
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from decimal import Decimal
from hexbytes import HexBytes

sqlite_file = "C:\\Users\\admin\\eth_database.db"
table_name_address = 'transactions'   # name of the table to be queried
table_name_block = 'blocks'   # name of the table to be queried
from_address_col = 'column3'
to_address_col = 'column4'

root = Tk()

infura_url = 'https://mainnet.infura.io/v3/370041072d44445ab61247cd925e221b'
web3 = Web3(Web3.HTTPProvider(infura_url))

#for etherscan API
es = etherscan.Client(
    api_key='XHT1QMF1HM8QM1JQJA68WNPTJF2WP1JM84',
    cache_expire_after=5,
)

root.title("ETH Blockchain Explorer")
root.state('zoomed')
root.grid_columnconfigure(0,weight=1)
root.configure(background='#fff')
#root.maxsize(1600,900)

#opens all time ETH value chart HTML
def open_html():
    webbrowser.open("D:\eth_price_chart_alltime.html")

 
#user entry field and instruction
#user_entry_instruction = Label(root, text='Ethereum Blockchain Explorer', font='verdana 15 bold', padx=50, pady=10,background='#fff')
#user_entry_instruction.grid(row=0, column=0, sticky="w")

user_entry = Entry(root, width=89, font='calibri 14', background='gray90')
user_entry.grid(row=1, column=0, padx=50, pady=10, sticky="w")

spacer_label = Label(root, anchor='w', padx=50, pady=5,background='#fff')
spacer_label.grid(row=3,sticky='w')


#Live blockchain info label
live_label = Label(root, anchor="w", font='verdana   15 bold', padx=50, pady=5,background='#fff')
live_label.grid(row=4,column=0, sticky="w")

#Clock
def livetime():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    live_label.config(text='Live Blockchain Information ' + time)
    root.after(1000, livetime)
livetime()

#declaring the labels that shows the  info
live_information = Label(root, font='courier 14 ', padx=50, pady=5, anchor="w",background='#fff')
live_information.grid(row=5,column=0, sticky="w")

live_information2 = Label(root, font='courier 14 ', padx=50, pady=5, anchor="w",background='#fff')
live_information2.grid(row=6,column=0, sticky="w")

spacer_label2 = Label(root, anchor='w', padx=50, pady=5,background='#fff')
spacer_label2.grid(row=7,sticky='w')

#search results label above results box
search_results = Label(root, text='Search Results', font='verdana 15 bold', anchor='w', padx=50, pady=5,background='#fff')
search_results.grid(row=8,sticky='w')


#button for opening expanded ETH price historm
button_eth_price = ttk.Button(root, text="Expand Value History",
                     width = 62, command=open_html,  style="W.TButton")
button_eth_price.grid(row=8, column=0, padx=0,pady=5, sticky="e")


#font for textbox titles
bold_font=Font(family='courier', size=12, weight='bold')
bold_font_bigger=Font(family='courier', size=13, weight='bold')


#text box containing quried data
textbox = Text(root, font='courier 12', background='gray90')
textbox.grid(row=9, column=0, columnspan=1, padx=(50,0),pady=(5,25) , sticky=W+E)

#scrollbar for textbox
scr=Scrollbar(root,orient=VERTICAL, command=textbox.yview)
scr.grid(row=9, column=1, sticky=NS, padx=(0,50), pady=10)
textbox.config(yscrollcommand=scr.set)


#creating a style for the button
style = ttk.Style()
style.configure("W.TButton", font=('calibri',13, 'bold'))


photoImageObj = PhotoImage(file="eth_price_chart_30days.png")
graph = Label(root, image=photoImageObj, anchor='e', padx=(20),pady=10)
graph.grid(row=0, rowspan=8,sticky='e')

bannerImageObj = PhotoImage(file="banner.png")
banner = Label(root, image=bannerImageObj, anchor='w',pady=20, borderwidth = 0,highlightthickness=0)
banner.grid(row=0,sticky='w')


#######################################################################################################
'''
This function grabs live Ethereum blockchain data from the connected Infure Node.
Data is diosplayed in the top left of the program window.
'''
def updating_block_info():

    block_from_infura = web3.eth.getBlock('latest')

    formatted_time = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(block_from_infura['timestamp'])))


    eth_price = es.get_eth_price() #get price from etherscan
    eth_supply = web3.fromWei(es.get_eth_supply(), 'ether') #get eth supply from etherscan and convert to ether from Wei
    eth_supply_formatted = str("{:,.2f}".format(eth_supply)) #2 decimal places

    eth_price_float = float(eth_price['ethusd']) 
    eth_supply_float = float(web3.fromWei(es.get_eth_supply(), 'ether'))

    market_cap = str("{:,.2f}".format(round((eth_price_float*eth_supply_float),2)))

    difficulty_live = float(block_from_infura['difficulty'])
    difficulty_live_TH = str("{:,.2f}".format(difficulty_live*0.000000000001)) #converting difficulty to TeraHashs


    template_live = "{0:19}| {1:27}| {2:26}" # column widths

    #the first row of live information
    blocknum_live = str('Block: ' + str(block_from_infura['number']))
    txcount_live = str('Tx count in block: ' + str(web3.eth.getBlockTransactionCount('latest')))
    difficulty_live = str('Difficulty: ' + difficulty_live_TH + ' TH')
    first_row = (template_live.format(blocknum_live,txcount_live,difficulty_live))

    #The second row of live information
    price_live = str('ETH Value: $' + str(eth_price['ethusd']))
    supply_live = str('ETH Supply: ' + eth_supply_formatted)
    marketcap_live = str('Market Cap: $' + market_cap)
    second_row = (template_live.format(price_live,supply_live,marketcap_live))

    
    live_information.config(text=first_row)
    live_information2.config(text=second_row)

    root.after(15000, updating_block_info)
updating_block_info()


#######################################################################################################


#######################################################################################################
'''
This function takes in an Ethereum address and queries the below data
from the LOCAL SQLITE3 DATABASE CONTAINING 2020 FIRST 7 DAYS OF TRANSACTIONS,
AS a result this will only return data if the Ethereum address being queried was active (sending or receiving)
during the period of time the downloaded transactions are from.
It then formats it and prints it to the text box.
'''
def query_address():
    textbox.delete('1.0',END)
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    textbox.configure(font='courier 12')

    #n = str(user_entry.get())

    eth_balance = es.get_eth_balance(user_entry.get())
    eth_balance_ether_string = str(("{0:.6f}".format((web3.fromWei(eth_balance,'ether')))))

    eth_price = es.get_eth_price()
    eth_price_float = float(eth_price['ethusd'])
    eth_balance_float = float(web3.fromWei(eth_balance,'ether'))
    eth_address_value = str("{:,.2f}".format(round((eth_price_float*eth_balance_float),2)))

    
    textbox.insert('1.0', 'Current balance: '+eth_balance_ether_string+'    Ether\n')#+ '       ' + '\nEther Value:  $' + eth_address_value +' USD\n')
    textbox.insert('2.0', 'Ether Value:    $' + eth_address_value +'    USD\n\n')
    textbox.insert('3.0','\n')
    textbox.insert('4.0','\n')
    textbox.insert

    c.execute('SELECT * FROM {tn} WHERE {cn}="{t}"'.\
            format(tn=table_name_address, cn=from_address_col, t=str(user_entry.get())))

    all_rows = c.fetchall()

    template = "{0:11}|{1:27}|{2:46}|{3:46}|{4:14}" # column widths
    header = (template.format("BLOCK #", "TIMESTAMP", "FROM ADDRESS", "TO ADDRESS", "VALUE (ETH)")+"\n") # header
    textbox.insert('4.0', header)
    
    textbox.tag_add("BOLD","4.0","4.150")
    textbox.tag_config("BOLD", font=bold_font)


    #declaring string to be used in for loop                    
    blocknum=''
    timestampyo=''
    fromaddy=''
    toaddy=''
    valeth=''
    combined=''
    
    for row in all_rows:
        #print(row)
        blocknum=str(row[0])
        timestampyo=str(row[1])
        fromaddy=str(row[2])
        toaddy=str(row[3])
        valeth=str("{:.7f}".format(web3.fromWei(row[4], 'ether')))#str(web3.fromWei(row[4], 'ether'))

        combined = (template.format(blocknum,timestampyo,fromaddy,toaddy,valeth)+"\n")

        textbox.insert('5.0',combined)

    ##############################################
    #Go again but checking the "TO" address column
    ##############################################

    c2 = conn.cursor()

    c2.execute('SELECT * FROM {tn} WHERE {cn}="{t}"'.\
            format(tn=table_name_address, cn=to_address_col, t=str(user_entry.get())))

    all_rows2 = c2.fetchall()

    #declaring string to be used in for loop                    
    blocknum2=''
    timestampyo2=''
    fromaddy2=''
    toaddy2=''
    valeth2=''
    combined2=''
    
    for row in all_rows2:
        blocknum2=str(row[0])
        timestampyo2=str(row[1])
        fromaddy2=str(row[2])
        toaddy2=str(row[3])
        valeth2=str("{:.7f}".format(web3.fromWei(row[4], 'ether')))#str(web3.fromWei(row[4], 'ether'))#str(web3.fromWei(row[4], 'ether'))

        combined2 = (template.format(blocknum2,timestampyo2,fromaddy2,toaddy2,valeth2)+"\n")

        textbox.insert('6.0',combined2)
        
    #query_label = Label(root,text=print_records)
    #query_label.grid(row=3, column=2)
    
    conn.commit()
    conn.close()
    
#######################################################################################################

'''
This function takes an array of transaction hashes and checks the value of each transaction
Stores the values in an array and finds the highest value(largest value tx in block)
'''
def biggest_tx(transaction_hashes):
    tx_values = []

    #query_times = []

    for tx_hash in transaction_hashes:

        #start = time.time()
        tx = web3.eth.getTransaction(tx_hash)
        #end = time.time()
        tx_values.append(tx["value"])
        #query_times.append(end-start)

    highest_value = max(tx_values)
    index_of_largest = tx_values.index(max(tx_values))
    largest_tx_hash = HexBytes.hex(transaction_hashes[index_of_largest])

    #average_q_time = statistics.mean(query_times)
    #print(average_q_time)

    return highest_value, largest_tx_hash


#######################################################################################################
'''
This function takes in a block number and queries the below data
from the connected Infura Node, formats it and prints it to the text box.
'''
def query_block():
    textbox.delete('1.0',END)
    # Connecting to the database file
    #conn = sqlite3.connect(sqlite_file)
    #c = conn.cursor()

    n = int(user_entry.get())

    #Block
    block = web3.eth.getBlock(n)

    #This converts the time from seconds since unix epoch to a date-time timestamp
    formatted_time = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(block['timestamp'])))

    all_txs_hash = block["transactions"]


    if not all_txs_hash: #if the block contained no transactions
        highest_value_tx_in_block = 0
        hash_of_containing_transaction = '-'
    else:
        #calls function biggest_tx and passed an array of the tx hashes in the block being queried
        highest_value_tx_in_block, hash_of_containing_transaction = biggest_tx(all_txs_hash)

    eth_price = es.get_eth_price()
    eth_price_float = float(eth_price['ethusd'])
    dollar_value = str("{:,.2f}".format((eth_price_float*(float(web3.fromWei(highest_value_tx_in_block, 'ether'))))))
    
 

    blocknum=str(block["number"])
    timestampyo=str(formatted_time)
    sizebytes=str(block["size"])
    txcount=str(web3.eth.getBlockTransactionCount(n))
    nonce=str(block["nonce"])
    miner=str(block["miner"])
    gasused=str("{:,}".format(block["gasUsed"]))
    gaslimit=str("{:,}".format(block["gasLimit"]))
    difficulty=str("{:,.2f}".format(block["difficulty"]*0.000000000001))
    combined=''

    gasused_float = float(block["gasUsed"])
    gaslimit_float = float(block["gasLimit"])

    gasused_percent_of_limit = (100*(gasused_float/gaslimit_float))

    textbox.configure(font='courier 13')# = Text(root, font='courier 18', background='gray90')


    #inserting the data and making the titles bold
    textbox.insert('1.0', 'BLOCK #:............................. '+blocknum+'\n\n')
    textbox.tag_add("BOLD","1.0","1.36")

    textbox.insert('3.0', 'TIMESTAMP:........................... '+timestampyo+'\n\n')
    textbox.tag_add("BOLD","3.0","3.36")
    
    textbox.insert('5.0', 'SIZE (BYTES):........................ '+sizebytes+'\n\n')
    textbox.tag_add("BOLD","5.0","5.36")
    
    textbox.insert('7.0', 'TX COUNT:............................ '+txcount+'\n\n')
    textbox.tag_add("BOLD","7.0","7.36")
    
    textbox.insert('9.0', 'MINER:............................... '+miner+'\n\n')
    textbox.tag_add("BOLD","9.0","9.36")
    
    textbox.insert('11.0', 'GAS LIMIT:........................... '+gaslimit+'\n\n')
    textbox.tag_add("BOLD","11.0","11.36")
        
    textbox.insert('13.0', 'GAS USED:............................ '+gasused+'  ('+str("{:.2f}".format(gasused_percent_of_limit))+'%)'+'\n\n')
    textbox.tag_add("BOLD","13.0","13.36")
    
    textbox.insert('15.0', 'DIFFICULTY (TH):..................... '+difficulty+'\n\n')
    textbox.tag_add("BOLD","15.0","15.36")

    textbox.insert('17.0', '------------------------'+'\n\n')
    textbox.tag_add("BOLD","17.0","17.37")

    textbox.insert('18.0', 'LARGEST TRANSACTION WITHIN BLOCK:\n\n')
    textbox.tag_add("BOLD","18.0","18.36")

    textbox.insert('19.0', 'HASH:.................................'+str(hash_of_containing_transaction)+'\n\n')
    textbox.tag_add("BOLD","19.0","19.37")

    textbox.insert('20.0', 'VALUE:................................'+str((web3.fromWei(highest_value_tx_in_block, 'ether')))+' ETH'+ ' ($' +str(dollar_value)+')'+'\n\n')
    textbox.tag_add("BOLD","20.0","20.37")

    textbox.insert('21.0', '------------------------'+'\n\n')
    textbox.tag_add("BOLD","21.0","21.37")

    textbox.insert('23.0', 'All Transactions in block:'+'\n\n')
    textbox.tag_add("BOLD","23.0","23.37")

    for tx in all_txs_hash:
        formatted = HexBytes.hex(tx)
        textbox.insert('25.0', formatted+'\n\n')
        
    
    textbox.tag_config("BOLD", font=bold_font_bigger)
    
    #conn.commit()
    #conn.close()

#######################################################################################################


#######################################################################################################
'''
This function takes in a transaction hash and queries the below data
from the connected Infura Node, formats it and prints it to the text box.
'''
def query_tx_hash():
    textbox.delete('1.0',END)

    n = str(user_entry.get())
    
    tx = web3.eth.getTransaction(n)

    tx_receipt = web3.eth.waitForTransactionReceipt(n)
                     
    blocknum=str(tx["blockNumber"])
    fromaddy=str(tx["from"])
    toaddy=str(tx["to"])
    valeth=str(web3.fromWei(tx["value"], 'ether'))
    gas=str("{:,}".format(tx["gas"]))
    gasused = str("{:,}".format(tx_receipt["gasUsed"]))

    gas_float = float(tx["gas"])
    gasused_float = float(tx_receipt["gasUsed"])
    
    gasused_percent_of_limit = (100*(gasused_float/gas_float))
    
    gasprice_gwei=str(tx["gasPrice"]*0.000000001)#converting Wei to GWei, the unit for gas price
    gasprice_ether=str("{:,}".format(web3.fromWei(tx["gasPrice"], 'ether')))
    #gas_price_float = float(tx["gasPrice"]*0.000000000000000001)

    combinedtx=''

    #getting the block that the tx is in so we can get the tx confirmation timestamp
    block_tx = web3.eth.getBlock(tx["blockNumber"])

    #This converts the time from seconds since unix epoch to a date-time timestamp
    formatted_time_tx = str(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(block_tx['timestamp'])))

    textbox.configure(font='courier 13')

    textbox.insert('1.0', 'BLOCK #:.......'+blocknum+'\n\n')
    textbox.tag_add("BOLD","1.0","1.15")

    textbox.insert('3.0', 'TIMESTAMP:.....'+formatted_time_tx+'\n\n')
    textbox.tag_add("BOLD","3.0","3.15")

    textbox.insert('5.0', 'FROM:..........'+fromaddy+'\n\n')
    textbox.tag_add("BOLD","5.0","5.15")
    
    textbox.insert('7.0', 'TO:............'+toaddy+'\n\n')
    textbox.tag_add("BOLD","7.0","7.15")
    
    textbox.insert('9.0', 'VALUE:.........'+valeth+' ETH'+'\n\n')
    textbox.tag_add("BOLD","9.0","9.15")
    
    textbox.insert('11.0', 'GAS LIMIT......'+gas+'\n\n')
    textbox.tag_add("BOLD","11.0","11.15")

    textbox.insert('13.0', 'GAS USED.......'+gasused+'  ('+str(gasused_percent_of_limit)+'%)'+'\n\n')
    textbox.tag_add("BOLD","13.0","13.15")
    
    textbox.insert('15.0', 'GAS PRICE:.....'+gasprice_gwei+' GWei'+'('+gasprice_ether+' Ether)'+'\n\n')
    textbox.tag_add("BOLD","15.0","15.15")
    

    textbox.tag_config("BOLD", font=bold_font_bigger)

#######################################################################################################


#######################################################################################################
'''
This function takes a quick look at the user entry and decided if its a
block number, ETH address or TX hash and runs the appropriate function.
Currently quite rudimentary as it simply decides based on the length of the input.
'''
def query_function_picker():    
    target = str(user_entry.get())#input("please enter a valid ETH adress or ETH block number!\n")

    pattern_block = re.compile("^(\d{0,7})$") #When 10 million blocks will need up to 8 digits for block number("^(\d{0,8})$")
    pattern_address = re.compile("^([A-Za-z0-9]{42})")#addresses are 42 characters long
    pattern_tx = re.compile("^([A-Za-z0-9]{66}|[A-Za-z0-9]{64})$")#transactions are 66 charactters long, or 64 if the beginning'0x' is omitted
    
    #now check if the input in an address or block number or TX hash.
    #run appropriate function
    if (pattern_address.match(target)):
        query_address()
    elif (pattern_block.match(target)):
        query_block()
    elif (pattern_tx.match(target)):
        query_tx_hash()
    else:
        textbox.delete('1.0',END)
        textbox.insert('1.0','Invalid Entry, please enter a valid i)Block Number ii)ETH Address iii)Transaction Hash\n')
    
#######################################################################################################

#button for running the query
button_query = ttk.Button(root, text="Search", style="W.TButton",
                    command=query_function_picker, width = 98,)
button_query.grid(row=2, column=0, padx=50,pady=5, sticky="w")


 
root.mainloop()
