
# Introduction
## Install package
```shell
pip install linkedin_cat
```
## Preparation

- create file `linkedin_cookies.json`

- please use Chrome Extension `EditThisCookie` to export linkedin cookies to `linkedin_cookies.json`



##  Example Usage:

```python
from linkedin_cat.message import LinkedinMessage

# linkedin cookie file path
linkedin_cookies_json='./linkedin_cookies.json'
# headless mode
headless = False
# Ininialized LinkedinMessage
bot = LinkedinMessage(linkedin_cookies_json,headless)

# message to sent, use FIRSTNAME or FULLNAME to customized the message
message = "Hello FIRSTNAME,hope you are doing well. Glad to e-meet with you on linkedin"

# Send single request by url
url = "https://www.linkedin.com/in/chandlersong/"
bot.send_single_request(url,message)

# Send multi request by linkedin url list 
urls_list = [    
    	"https://www.linkedin.com/in/chandlersong/",
    	"https://www.linkedin.com/in/chandlersong/",
        ]

bot.send_multi_request(urls_list,message)
    
```

