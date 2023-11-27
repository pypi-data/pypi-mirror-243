# UPSRTC Bus Tracker
Unofficial python wrapper around UPSRTC internal API for planning bus journey.

## Prerequisites
- python > 3.9
- requests

## Usage
### Install library
- Install using pip.
```pip install python-upsrtc```
### Generate UPSRTC object
To generate a UPSRTC object, you can use the following code:
```python
from python-upsrtc import UPSRTC as UP
u = UP()
```

### Get Bus Stops Data
To get bus Stops data, use the following code:
```python
u.get_bus_stop()
# raises NOJourneyFoundError if no bus are found
# raises InvalidSearchSettingsError if search settings are not filled correctly or are empty.
print(u.bus_stops)
# List(BusStop)
```
It fetches a list of BusStop object stored in bus_stops attribute\
See [BusStop](docs.md#busstop) for its related methods and attributes.

### Find Buses between stations.
```python
from datetime import datetime 
#set start station
u.set_start_station("7381") # get station code from bus stops data
u.set_end_station("8778")
u.set_start_date( datetime.now() ) # Set the start date (requires a datetime object as date )
u.find_buses()
print( u.journey )
# List( Ticket )
```
It fetches a list of Ticket attributes stored in journey attribute.\
See [Ticket](docs.md#ticket) for its related methods and attributes.

## TODO
- [ ] Implement custom rotating proxy
- [ ] Automatic proxy fetching.
- [ ] Include Fare distribution in Ticket object.

## Documentation
Checkout the documentation [here](https://github.com/mohdsabahat/python-upsrtc/blob/main/docs.md)

## Authors
- Mohd Sabahat : <mohd.sabahat123@gmail.com>

## Notice
**NOTE : I am not affiliated or endorsed with [UPSRTC](https://www.onlineupsrtc.co.in/). This is just an API wrapper around their already existing internal, and i am not responsible for any knd of damage that might cause using this code.**