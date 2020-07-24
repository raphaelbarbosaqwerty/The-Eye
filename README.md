# The-Eye
```
           _ . - = - . _             
       . "  \  \   /  /  " .         
     ,  \                 /  .       
   . \   _,.--~=~"~=~--.._   / .     
  ;  _.-"  / \ !   ! / \  "-._  .    
 / ,"     / ,` .---. `, \     ". \   
/."   `~  |   /:::::\   |  ~`   ".\  
\`.  `~   |   \:::::/   | ~`  ~ ."/  
 \ `.  `~ \ `, `~~~" ,` /   ~`." /   
  .  "-._  \ / !   ! \ /  _.-"  .    
   ./    "=~~.._  _..~~=`"    \.     
     ,/         ""          \,       
 LGB   . _/             \_ .         
          " - ./. .\. - "            
___________.__             ___________             
\__    ___/|  |__   ____   \_   _____/__.__. ____  
  |    |   |  |  \_/ __ \   |    __)<   |  |/ __ \ 
  |    |   |   Y  \  ___/   |        \___  \  ___/ 
  |____|   |___|  /\___  > /_______  / ____|\___  >
                \/     \/          \/\/         \/ 
```
## What's this about?

TheEye is a reconnaissance tool that was writte in Python with Slack and Nmap integrated. When the tools ends te scan they sent to Slack workspace with a notification push all information about the host. Why I'm not using Masscan(Amazing tool)? I really don't know, just decided use Nmap.

## Requeriments
* Nmap
* Python 3.x
* Slack Workspace
## Installation
To use this tool you need [Nmap](https://github.com/nmap/nmap)  
Clone the tool from Github  
`$ git clone https://github.com/raphaelbarbosaqwerty/The-Eye.git && cd The-Eye/`  
  
Install the dependencies:  
`$ pip3 install -r requirements.txt`

## Configuration
1. For use this tool you need to create a Slack Workspace at https://slack.com/  
2. Create a channel on your Workspace.
3. Generate a webhook URL 
    * https://api.slack.com/apps
    * Browse to Incoming Webhooks and create a new Webhook.
    * Copy the created Link
    * E.g: https://hooks.slack.com/services/XXXXXXX/BF0XXXXME/XXXXXXXXXXXXX
4. Open your `config.py` and set your new Webhook.
5. It's ready to use.

## Usage
`$ python3 theeye.py -h`
| Short Form   |      Long Form      |  Description |
|----------|:-------------:|------:|
| -h |  --help | Show all commands |
| -u |  --url | Scan only one host |
| -U |    --urlslist   |   Scan multiple hosts from file |
| -t | --threads |    Define the number of threads. Default 5 |
| -T | --timeout |    Timeout to check if the port is closed. Default 20000 |

## About Nmap
TheEye are using the most basic command for Nmap.    
1. Get open Ports  
  `nmap -p- --min-rate=20000 -T4 ip_server`    
2. Scan the ports  
  `nmap -A -p$openPorts ip_server`  
3. Send all the information to Slack Workspace  

## Images && Time
1. Working  
![Example1](https://raw.githubusercontent.com/raphaelbarbosaqwerty/The-Eye/master/Imgs/TheEyeExample2.png)  
2. Time  
![Example2](https://raw.githubusercontent.com/raphaelbarbosaqwerty/The-Eye/master/Imgs/TheEyeExample2.1Time.png)
3. Push Notification to Slack Workspace  
![Example3](https://github.com/raphaelbarbosaqwerty/The-Eye/blob/master/Imgs/TheeyeExample.png?raw=true)  
4. In Slack Workspace  
![Example4](https://raw.githubusercontent.com/raphaelbarbosaqwerty/The-Eye/master/Imgs/TheEyeExample3.png)  

## Feedback and Issues?
Are welcome. Please feel free to file an issue on https://github.com/raphaelbarbosaqwerty/The-Eye/issues

## Tool based && Integration
* Tool based on the following tools
  1. https://github.com/clirimemini/Keye
  2. https://github.com/yassineaboukir/sublert