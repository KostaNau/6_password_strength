# Password Strength Calculator


## Description

The script evaluate power of your password with score from 0 to 10. If you have connection to the internet or you have personal blacklist, script will try to find password in remote collection blacklists (<https://github.com/danielmiessler/SecLists>) or your local blacklist (optional).


## How to use

**Defaul mode:** Just run the script ```password_strength.py```

If you want to additional check in your private black list, run the script with optional argument: ```-local``` and determine filename of your blacklist or path.


## Example
**Optional mode:**
```
user$ python3 password_strength.py -l yourlist.txt

>>> Checking your connection to the Internet...
>>> Connected.
>>> City of Brith:
>>> Date of Brith:
>>> Family Name:
>>> Given Name:
>>> Your Phone Number:
>>> Type your password:
>>> Calculating strength of your password, please wait...
Strength of your password: 0 of 10
```


## Build with
+[Requests](http://docs.python-requests.org/en/master/) - for receiving remote blacklists


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
