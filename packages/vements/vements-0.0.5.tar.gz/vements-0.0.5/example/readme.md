## Python Example for Vements

This directory contains an example of how to use the Vements Client Library for Python to create a client and use that client to create a new participant, scores for that participant, and finally view a scoreboard with those scores.

### Prerequisites

Before you can continue, you must have the following:

- API key
- Project ID
- Scoreboard ID

To create these resources and get their IDs, create a trial or paid account at [Vements](https://vements.io).  Then log into the dashboard and create a new project.  Once you have a project, you can create an API key and a scoreboard.  Important: create a "read-write" API key.  The example will not work with a "read-only" API key.

### Running the Example

To run the example, first clone the repo:

```shell
$ git clone https://github.com/vements/client-py
```

Then update the `example/example.py` file to use your API key and the ID of your project and scoreboard.  Change the following lines:

```python
API_KEY = "put your API key here"
PROJECT_ID = "put your project ID here"
SCOREBOARD_ID = "put your scoreboard ID here"
```

Then run the example:

```shell
$ cd client-py
$ python example/example.py
```