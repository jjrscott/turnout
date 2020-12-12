# Turnout

Turnout converts a JSON file representing a vote into a square chart which can represent both the voter share of each choice and those who didn't vote at all. These values are often missed from normal line or pie charts.

As can be seen below, while Hillary Clinton did win the popular vote, neither of the candidates managed to persuade the populous to vote enmass.

<p align="center"><img alt="2016 United States presidential election" src="output/2016 United States presidential election.svg" width="400"></p>

### Usage

```shell
python3 turnout.py examples/*.json -output output -size 600
qlmanage -t -s 600 -o output output/*.svg
```



### Input files

The input JSON files have the format:

```js
{
  "choices": [
    {
      "color": // string SVG color value
      "title": // string: First place title
      "value": // number: First place percentage or absolute count
    },
    {
      "color": // string SVG color value
      "title": // string: Second place title
      "value": // number: Second place percentage or absolute count
    }
  ],
  "title": // string: Title of the chart
  "total": // number: Total elegible to vote. Choice values will be treated as an absolute count
  "turnout": // number: Percentage of those eligible to vote who did so. Choice values will be treated as percentage
}
```



### Examples

All these charts were generated from data in the [examples](examples) folder.


<p align="center"><img alt="2011 United Kingdom Alternative Vote referendum" src="output/2011 United Kingdom Alternative Vote referendum.svg" width="300"> <img alt="2014 Scottish independence referendum" src="output/2014 Scottish independence referendum.svg" width="300"> <img alt="2016 United Kingdom European Union membership referendum" src="output/2016 United Kingdom European Union membership referendum.svg" width="300"> <img alt="2017 United Kingdom general election" src="output/2017 United Kingdom general election.svg" width="300"> <img alt="British Parliamentary approval for the invasion of Iraq" src="output/British Parliamentary approval for the invasion of Iraq.svg" width="300"> <img alt="General election 2019 Eastleigh" src="output/General election 2019 Eastleigh.svg" width="300"></p>