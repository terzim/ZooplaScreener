# Zoopla Screener

Building on my previous stock screener, and because at some point I will have to buy a flat in London, I coded this little Screener.  

What it does:

Leaning on the public [Zoopla Developer API](https://developer.zoopla.co.uk/), it runs a query for the flats and sends it straight away in a formatted table to my email address.

## Installation Instructions
Tested with, and assumes you already have at your disposal:
- Ubuntu 16.04;
- Anaconda Python 3.5.3 
- Gmail email server. 

Install git
```
sudo apt-get update
sudo apt-get install git
```

Copy the repository on your computer and rename the sample config file
```
git clone https://github.com/terzim/ZooplaScreener.git
cd ZooplaScreener
mv sample_zoopla_config.ini zoopla_config.ini
```
Install the python requirements
```
(sudo) conda install --yes --file requirements.txt  # If using Anaconda Python distribution
```
or
```
(sudo) pip3 install -r requirements.txt # If using a standard Python3 distributions
```

## Get your API key
First thing first you need to [open an account with Zoopla](https://developer.zoopla.co.uk/member/register/) and [get an API key](https://developer.zoopla.co.uk/member/register/)

## Configuration
Open the ```zoopla_config.ini``` file in your favourite text editor. Edit the configuration parameters accordingly.

The instructions are [available at this link](https://developer.zoopla.co.uk/docs/Property_listings) 

### Config file example

Sample config file:
```
[api_data]
api_key =

[flat_data_str]
area =
order_by =
ordering =
listing_status =
furnished =
property_type =
new_homes =
chain_free =
keywords =
summarised =

[flat_data_num]
radius =
include_sold =
include_rented =
minimum_price =
maximum_price =
minimum_beds =
maximum_beds =
listing_id =
branch_id =
page_number =
page_size =

[output]
output_fields =

[email_data]
send_email =
sender =
recipient =
pwd_sender =
server_name =
server_port =
```


### Run the screen
The screen can be run one-off
```
python ZooplaScreener.py
```
or - in alternative - scheduled for periodical execution via crontab (and - possibly - a VPS). For instructions to setup crontab on a VPS, read a [shorthand guide here](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps). 

### Credits

Property information powered by Zoopla

[<img src="https://www.zoopla.co.uk/static/images/mashery/powered-by-zoopla-150x73.png">](http://www.zoopla.co.uk)

