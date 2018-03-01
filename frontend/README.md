# Frontend

This application provides a Web UI which provides users with the ability to create tests, add questions, and render it into an AMC project that can be converted to PDF and distributed to students.

## Configuration

There are two environment variables that can be set at build time.  `REACT_APP_API_ROOT` should be set to the URL where the Python backend webserver will be listening (defaults to `localhost`).  `REACT_APP_API_PORT` should be set to the port on which that API is listening (defaults to 4545).

## Installation

1. Install NodeJS (version 8.5.0 or higher) and Yarn
1. `yarn`
1. `yarn start`
