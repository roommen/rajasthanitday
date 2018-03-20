from os import system

#Subscribe to the right stream
system("multichain-cli aadhaar subscribe demo")

# List the stream items
system("multichain-cli aadhaar liststreamitems demo")
