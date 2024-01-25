# Automaticly solve the problem of 'Ping timed out' using selenium when pinging github.com

## Description

To solve the problem of 'Ping timed out' automatically when pinging github.com and cloning projects using git without manual complex configuration. 

By using selenium to crawl the available IPs of 'github.com' and 'github.global.ssl.fastly.net', the script rewrites the 'hosts' file to add the former two IPs automatically and refresh the DNS resolution cache.

## Dependencies
- selenium
- pyyaml

## Installation

Use `pip install selenium pyyaml` to install the required packages. Note that you need to download EdgeDriver/Chromedriver(depending on your own choice, in this script we use the first one) of the same version as your current browser and then add the driver path to your environment variables.

## Usage

Run git_network_srcipt.py in the command line(cmd) with administrator privileges and do not run it directly.

*Example:*

FIRST STEP: start cmd with administrator privileges
```
> e:
> cd path/to/script
> conda activate base
> python git_network_script.py
```
