# Ethereu-Blockchain-Explorer-FYP
Final Year Project - Ethereum blockchain explorer. READ README!

The EtherPrice CSV will only be updated when the program is run, hence the ETH price chart will be created with out-of-date data if the program has not been run in some time. Up-to-date ETH price data is available in CSV format from https://etherscan.io/chart/etherprice

Due to the nature of the Ethereum blockchain constantly expanding in size (TB's), without a dedicated machine running an ETH node, and storing up-to-date transaction data on all ETH addresses the full ETH address transaction history will not be available. For demonstration purposes a database file named 'eth_database' is used, containing transactions from the first 5 minutes of 01-01-2020. Querying an address that was active during this time-period will return all transaction data of that address during the time period. To be sure 
