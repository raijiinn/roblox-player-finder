import requests
import time
import threading
userid = '1088819236'
placeid = '7115420363'
Found = False
cookie =  "enter ROBLOSECURITY cookie here"
cookies = {".ROBLOSECURITY":cookie} # set cookie dictionary/json
image = requests.get(f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&width=48&height=48&format=png").url # get user image
#xheaderthing = requests.post(f"https://auth.roblox.com/v2/signup",cookies=cookies).headers["x-csrf-token"] # get the x-csrf-token header
#headers = {"x-csrf-token": xheaderthing} # set headers for request   
# commented this above because i realised i didnt need the headers lol
    

def findplayer(placeid,idx):
   global Found
   for i in range(10): # 10 retries if ratelimited etc. 
    try:   
        print(idx)    
        serverindex = requests.get(f'https://www.roblox.com/games/getgameinstancesjson?placeId={placeid}&startIndex={str(idx)}',cookies=cookies)  # get server     
        serversize = serverindex.json()['TotalCollectionSize']
        currentsize = len(serverindex.json()['Collection'])      
        for i in range(11): # this is for the last servers they dont have 10 servers in the list so we check if we actually hit the end by looping through it 10 times and seeing if we get any lists with data if not then it will return found or it will end 
            if currentsize < 10: # checks size of list
                serverindex = requests.get(f'https://www.roblox.com/games/getgameinstancesjson?placeId={placeid}&startIndex={str(idx-i)}',cookies=cookies)   # sets back index   
                if len(serverindex.json()['Collection']) > 0:
                    break   
        for servers in serverindex.json()['Collection']:
            for players in servers['CurrentPlayers']:
                if players['Thumbnail']['Url'] == image:                
                    print('found ' + servers['Guid'])
                    Found = True  # found variable for breaking loop                   
        return serversize
        




    except Exception as ex:
        print(ex)    
serversize = findplayer(placeid,1) # gets length of all servers
for i in range(0,serversize,10): # loops through all servers with a increment of 10
    if Found == True:
        break
    finderthread = threading.Thread(target=findplayer, args=[placeid,i]) # makes thread so we can run multiple checks on different servers and not have to wait for one to finish
    finderthread.daemon = True
    finderthread.start() # start thread
  

