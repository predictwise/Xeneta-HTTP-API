# A solution to HTTP-based API

## Requirements

Information about setup environment, including:

* Python 3.7 (other Python 3.x should be fine as well)
* Flask
* psycopg2
* Docker container (please refer to the initial setup of this assignment provided by Xeneta team)

## Assumption

Assume that `origin` and `destination` are obtained from database and hence, they do not contain special characters(e.g., >, <, !) and other errors

## Questions

I am not sure whether the `origin` is always an individual 5-character port code ? 

According to the testing demo provided by Xeneta team, it shows that the `origin` is a 5-character port code, therefore, I only considered about the scenario where the input of `origin` is a 5-character port code 

## Run the service

    cd Xeneta-HTTP-API
    python api.py
    

## Testing examples

Testing example 1: 

`destination` is a 5-character port code (e.g., `GBFXT`)

    curl "http://127.0.0.1:5002/rates?date_from=2016-01-01&date_to=2016-01-05&origin=CNSGH&destination=GBFXT"

    [
        {
            "average_price": 1098.0,
            "day": "2016-01-01"
        },
        {
            "average_price": 1098.33,
            "day": "2016-01-02"
        },
        {
            "average_price": null,
            "day": "2016-01-04"
        },
        {
            "average_price": 1097.67,
            "day": "2016-01-05"
        }
    ]

Testing example 2:

`destination` is a leaf slug (e.g., `uk_main`)

    curl "http://127.0.0.1:5002/rates?date_from=2016-01-01&date_to=2016-01-05&origin=CNSGH&destination=uk_main"

    [
        {
            "average_price": 1217.83,
            "day": "2016-01-01"
        },
        {
            "average_price": 1218.17,
            "day": "2016-01-02"
        },
        {
            "average_price": null,
            "day": "2016-01-04"
        },
        {
            "average_price": 1217.17,
            "day": "2016-01-05"
        }
    ]


Testing example 3:

`destination` is a parent slug (e.g., `north_europe_main`)

    curl "http://127.0.0.1:5002/rates?date_from=2016-01-01&date_to=2016-01-05&origin=CNSGH&destination=north_europe_main"

    [
        {
            "average_price": 1111.92,
            "day": "2016-01-01"
        },
        {
            "average_price": 1112.0,
            "day": "2016-01-02"
        },
        {
            "average_price": null,
            "day": "2016-01-04"
        },
        {
            "average_price": 1141.62,
            "day": "2016-01-05"
        }
    ]


Testing example 4:

`destination` is a grandfather slug (e.g., `northern_europe`)

    curl "http://127.0.0.1:5002/rates?date_from=2016-01-01&date_to=2016-01-05&origin=CNSGH&destination=northern_europe"

    [
        {
            "average_price": 1475.9,
            "day": "2016-01-01"
        },
        {
            "average_price": 1475.89,
            "day": "2016-01-02"
        },
        {
            "average_price": null,
            "day": "2016-01-04"
        },
        {
            "average_price": 1463.02,
            "day": "2016-01-05"
        }
    ]
    

## Extra details

* 30 minutes for studying the table schema, relations between tables, data samples, requirements of the assignment, setup environment etc
* 2 hours for coding
* 30 - 40 minutes for unit tests and fixing bugs
* 25 minutes for writing this `README.md`
