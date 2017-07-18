# Integration tests for AtomicBoard

The aim of this project is to cover by integration tests the web service AtomicBoard. The stage server is available by address
[atomicboard.devman.org](http://atomicboard.devman.org).


Tests cover the main scenarios of using the service:

- Loading from the server and displaying a list of current tickets
- Drag and drop ticket from one column to another
- Editing an existing ticket
- Marking the ticket as solved
- Creating a new ticket

## Installation

```
$ pip install -r requirements.txt
$ npm install
```

## Running the tests

```
$ pytest
```

## Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
