ABOUT
============
The python-eigen-ingenuity library is used to query data from the Eigen Ingenuity system for use in the python environment, and to upload data to the 

REQUIREMENTS
============

Installing python-eigen-ingenuity requires python 3

INSTALL
=======

Install python 3, then in the terminal run:

```
pip install python-eigen-ingenuity
```

All third party library requirements should be automatically acquired.

GETTING STARTED
-------
Begin by Importing the module with

```
import eigeningenuity as eigen
```

To use this module, you must first set an Ingenuity server to query, and a datasource within the server.

For example, with Ingenuity instance "https://demo.eigen.co/" and datasource "Demo-influxdb",


```
server = eigen.EigenServer("https://demo.eigen.co/")
demo = eigen.get_historian("Demo-influxdb",server)
```
Alternatively, it is possible to set the Ingenuity instance as the environmental variable "EIGENSERVER",
```
os.environ["EIGENSERVER"] = "https://demo.eigen.co/"
demo = get_historian("Demo-influxdb")
```

Alternatively, it is possible to set the Ingenuity instance as the environmental variable "EIGENSERVER",
```
os.environ["EIGENSERVER"] = "https://demo.eigen.co/"
demo = get_historian("Demo-influxdb")
```

If the datasource of interest is the default datasource for the ingenuity instance, it can be omitted:

```
os.environ["EIGENSERVER"] = "https://demo.eigen.co/"
demo = get_historian()
```

DATA FORMAT
===

Once the server and datasource have been configured, the historian data can be queried through functions we define in
the EXAMPLE FUNCTIONS section.

These functions can be used to query a single tag, or multiple tags at once. A tag in ingenuity with the form "datasource/tagname", 
we query with, for example:

```
datasource = eigen.get_historian("datasource")
tagdata = datasource.getCurrentDataPoints("tagname")
```

DataPoint
---

Most functions return datapoint objects, each of which contains a Value, Timestamp, and status as below

``````
<class 'eigeningenuity.historian.DataPoint'>
35 @ 2022-05-30 11:02:13 UTC - OK
``````

This can be parsed with the following:

``````
demo.getCurrentDataPoints(...)

value = datapoint.value (35)
timestamp = datapoint.timestamp (1653904933.0)
utcTime = datapoint.datetime (2022-05-30 11:02:13)
status = datapoint.status (OK)
``````
Here the timestamp field is the timestamp in epoch seconds (seconds since January 1st 1970), and the utcTime field is a
python datetime object

AggregateDataSets
---

The GetAggregates and getAggregateIntervals functions return data in AggregateDataSets rather than DataPoints, for example,
in the case we requested all aggregates we might receive a set like:

```
AggregateDataSet[ start:2022-06-01 10:27:15 UTC end:2022-06-01 10:42:45 UTC - min:   33.00000     max:   38.00000     avg:   35.66667     var:   3.15476      stddev:   1.77616      numgood: 57   numnotgood: 0   ]]
```

And in this case, if we requested only min we would receive:

```
AggregateDataSet[ start:2022-06-01 10:27:15 UTC end:2022-06-01 10:42:45 UTC - min:   33.00000     max: None   avg: None   var:   0.00000      stddev:   0.00000      numgood: None   numnotgood: None   ]]
```

These sets can be parsed with the following:

``````
AggSet = demo.getAggregates(...)

aggStart = AggSet.start     
aggEnd = AggSet.end    
aggMin = Aggset.min 
aggMax = Aggset.max
aggAvg = Aggset.avg
aggVar = Aggset.var
aggStdDev = Aggset.stddev
aggNumGood = Aggset.numgood
aggNumBad = Aggset.numnotgood


``````

Query Multiple tags
===

if multiple tags are queried in a single request, the data will be returned as a dictionary, with the tag IDs as its keys,
the individual dictionary entries will retain the same format returned when querying a single tag
____

FUNCTIONS
==
Data Queries
===

#### The following functions are designed to help the user pull and process data from historians into a python environment

list_historians
----

Find all historians on the instance
```
from eigeningenuity import list_historians
list_historians(eigenserver)
```
Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a list of strings

get_default_historian_name
---
Find the name of the default historian of the instance, if one exists
```
from eigeningenuity import get_default_historian_name
get_default_historian_name(eigenserver)
```
Where:
- (Optional) eigenserver is the ingenuity instance of interest (If omitted will look for environmental variable EIGENSERVER)

Returns a string, or None

getCurrentDataPoints
----
Find the most recent raw datapoint for each tag
```
demo.getCurrentDataPoints(tags)
```
Where:
- tags is a list of IDs of tags to query

Returns one datapoint object per tag

countPoints
----
Find the number of datapoints in the given time frame
```
demo.countPoints(tag, start, end)
```
Where:
- tags is a list of IDs of tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window

Returns one integer per tag

getInterpolatedRange
----

Find a number of interpolated points of a tag, equally spaced over a set timeframe
```
demo.getInterpolatedRange(tag, start, end, count)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- count is the total number of points to be returned

Returns a list of count-many datapoints per tag

getInterpolatedpoints
----

Find datapoints at given timestamps
```
demo.getInterpolatedPoints(tags, timestamps)
```
Where:
- tags is a list of IDs of the tags to query
- timestamps is a list of timestamps at which to query data

Returns a list of datapoints (one at each timestamp) per tag

getRawDataPoints
----

Find the first n Raw datapoints from a time window
```
demo.getRawDataPoints(tags, start, end, count)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) count is the maximum number of raw datapoints to return. (default is 1000)

Returns a list of count-many datapoints per tag

getAggregates
----

Finds a set of aggregate values for tags over a timeframe
```
demo.getAggregates(tags, start, end, count, aggfields)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) count is the number of divisions to split the time window into (i.e. if time window is one day, and count is 2,
we return separate sets of aggregate data for first and second half of day). omit for count=1
- (Optional) aggfields is a list of aggregate functions to calculate, a subset of 
["min","max","avg","var","stddev","numgood","numbad"].  Leave blank to return all aggregates.

Returns a list of count-many Aggregate Data Sets per tag

getAggregateIntervals
----

A variation of getAggregates which finds aggregates on fixed length intervals dividing the overall window
```
demo.getAggregateInterval(tags, start, end, interval, aggfields)
```
Where:
- tags is a list of IDs of the tags to query
- start is the datetime object (or epoch timestamp in ms) of the beginning of the query window
- end is the datetime object (or epoch timestamp in ms) of the end of the query window
- (Optional) interval is the length of the sub-intervals over which aggregates are calculated, it accepts values such as ["1s","1m","1h","1d","1M","1y"]
being 1 second, 1 minute, 1 hour etc. Default is whole time window.
- (Optional) aggfields is a list of aggregate functions to calculate, a subset of 
["min","max","avg","var","stddev","numgood","numbad"]. Default is all Aggregates.

Returns a list of Aggregate Data Sets (One per interval) per tag

listDataTags
----

Find all tags in datasource, or all tags in datasource that match a search parameter
```
demo.listDataTags(match)
```
Where:
- (optional) match is the regex wildcard to match tags to (i.e. DEMO* will match all tags beginning with DEMO, \*DEMO* will match
all tags containing DEMO, and *DEMO will match all tags ending with DEMO) (Leave blank to return all tags in historian)

Returns a list of strings

getMetaData
----

Find units, unitMultiplier and description of each tag
```
demo.getMetaData(tags)
```
Where:
- tags is a list of IDs of tags to query

Returns a dict with keys [units, unitMultiplier, description] per tag

Data Upload
===

#### The following functions are intended for users to update/create historian tags using data processed/loaded in python.


createDataTag
----

Creates a datatag with a specified ID, Unit type/label, and Description
```
demo.createDataTag(Name, Units, Description)
```
Where:
- Name is the unique ID/Identifier of the tag
- Units is the unit specifier of the data in the tag e.g. "m/s","Days" etc. (This will be shown on axis in ingenuity trends)
- Description is text/metadata describing the content/purpose of the tag (This will show up in search bar for ingenuity trends)

Returns a boolean representing success/failure to create tag

writeDataPoints
----

Writes sets of datapoints to the historian
```
from eigeningenuity.historian import DataPoint

dataPoints = []
point = DataPoint(value, timestamp, "OK")
dataPoint = {tagName: point}

dataPointList.append(dataPoint)

demo.writeDataPoints(dataPointList)
```
Where:
- value if the value of the datapoint at the timestamp
- timestamp is the datetime object (or epoch timestamp in ms) of the point
- "OK" is the status we give to a point that contains non-null data

Returns a boolean representing success/failure to write data

____


LICENSE
-------
With the datasource set, the historian data can be queried with functions such as,
```
demo.getInterpolatedRange(tag,start,end,points)
demo.getCurrentDataPoints(tag)
demo.listDataTags()
```
Where:
- tag is the name of the tag to query
- start is the epoch timestamp (ms) of the beginning of the query window
- end is the epoch timestamp (ms) of the end of the query window
- points is the number of points to be returned

Each function will return an list, each element consisting of list of a value, timestamp and status, corresponding to a single point of data

To convert a Datetime (UTC or Local) to epoch, or vice-versa, you can use this tool: https://www.epochconverter.com/

LICENSE
-------
Apache License 2.0

 Copyright 2022 Eigen Ltd.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
