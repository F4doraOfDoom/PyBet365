# About PyBet365

PyBet365 is a Selenium based crawler for the bet365.com betting website.
It utilizes Selenium's ChromeDriver and BeautifulSoup4 in order to parse the In-Plays,
and display real-time betting match data.

It also has built-in proxy support, in order to avoid banning.
PyBet365 uses free proxies from the internet, so please use at your own discretion. 

## Great, how do I use it?
Make sure you have the right dependencies installed.
This project uses:
```
beautifulsoup4 = 4.7.1
selenium = 3.141.0
requests = 2.22.0 		#only if you use proxies
```
### Dependencies

I just downloaded the newsest version. Older versions of Selenium and requests would probably work as well.

### Installing PyBet365

First, download the repository
```git
git clone https://github.com/F4doraOfDoom/PyBet365
```
Then, cd into the directory
```bash
cd PyBet365
```
Run the script!
```bash
python3.7 bet365_scraper.py
```

## Options

This first version of PyBet365 has some flags you can set in order to change the behaviour of the script.

### Proxies

By default, PyBet365 does not use proxies. This is because they slow the script down, as the proxies available are used by many people.
In order to use proxies, add the flag:
```bash
---use-proxies
```
This tells the script to download a list of proxies from the internet. The proxies are free, but still, caution is advised. Use at your own risk. From my testing, it has helped me avoid getting my own IP blocked from bet365.com

### Headless
By default, the script runs in chrome's --headless mode. This means that you wont be able to see the current ChromeDriver instance. For example, if you're viewing this from a Chrome brower, you're looking at a ChromeDriver instance. Being headless makes the script work better in the background, and save resources.

If you want to disable that, add:
```bash
--no-headless
```
This tells the script to run in headfull mode. Great for debugging, and seeing what the script actually does realtime.

### Parsing
By default, the script reparses the website every 3 seconds. This was arbitrarily chosen. 

To change this, use:
```bash
-r/--refresh <unit of time (seconds)>
```
