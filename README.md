# Auto Multiple Choice Web UI

This application serves as a web-based interface for the [Auto Multiple Choice](https://www.auto-multiple-choice.net/) application.  It allows users to create their own questions, generate tests using them, and grade the tests once students have completed them.

## Reference

* [AMC Command Line Reference](https://www.auto-multiple-choice.net/auto-multiple-choice.en/commands.shtml)
* [AMC Command Line Usage Guide](https://project.auto-multiple-choice.net/projects/auto-multiple-choice/wiki/Using_AMC_in_command_line_only)

## Implementation

The system consists of two separate applications: the **backend** and the **frontend**.  Both of these are bundled together inside of the Docker container, and the backend essentially serves the static frontend directly.  It is designed to be deployed on a server that all users can access, but that the students taking the generated quizzes do not.

There is currently no login or authentication system in place, and all created questions are available publicly.  In the future, a login system could be created and more advanced levels of question storage (private to a single user, to select users, etc.) can be put in place.

### Backend

The backend is a Python application that has the main purpose of wrapping the `auto-multiple-choice` command line and interfacing with the MongoDB instance.  It starts up a Flask webserver that exposes all of the API routes, and it also serves the static frontend alongside them.

The backend is designed to be stateless, with the only state in the entire application being limited to the database.  For many API endpoints that involve AMC commands internally, temporary project directories must be created.  However, these directories are never meant to be accessed after the request that created them is finished.

All created questions are stored in a database that allows other users to pick from them and use them in their own tests.  In addition, the schemas of all created tests (containing all selected questions and other config provided by the user) are stored when tests are generated.  Using this stored spec, exact duplicates of the created tests can be regenerated in temporary project directories for grading purposes.  By deterministically seeding the random number generator that AMC uses to shuffle questions and perform other psudeo-random tasks, it's possible to re-create exact copies of tests using this method.

### Frontend

The frontend is a React application that provides users with a web interface for interacting with the backend.  It is compiled into a static HTML and JavaScript distrubution and served directly from the backend.  Three main functionaities are currently included:

* Creating Questions
* Generating and Downloading Quizzes
* Uploading + Grading Tests

The goal is to provide users with limited technical expertise interact with Auto Multiple Choice in a meaningful way without requiring them to learn a lot about how it works internally.  It aims to provide a simple interface that defaults to the minimum amount of information required to define, generate, and grade basic quizzes.

## Configuration

Configuration for this application is handled via environment variables.  The full list of available variables are listed below along with their defaults and a description of their functionality:

| Variable         | Default   | Description                                                                                                                                                                                                   |
|------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `MONGO_HOST`     | localhost | The host on which the MongoDB instance for the application is running.                                                                                                                                        |
| `MONGO_PORT`     | 27017     | The port on which the MongoDB instance for the application is running.                                                                                                                                        |
| `MONGO_USER`     | *unset*   | If the MongoDB instance is set up with authentication, this is the username that will be used when authenticating.  If left unset, the application will assume that no database authentication is being used. |
| `MONGO_PASSWORD` | *unset*   | If the MongoDB instance is set up with authentication, this is the password that will be used when authenticating.  If left unset, the applicat                                                               |

## Manual Installation

1. Install Python3 and Node.JS version 8.5.0 or higher
1. Install and set up a MongoDB instance for use with storing questions and tests
1. Make sure you have the `auto-multiple-choice` command line installed on your machine as well as the `texlive-fonts-recommended` package.
1. Install dependencies for the frontend: `cd frontend && yarn`
1. Build a static version of the frotend: `yarn build`
1. Copy a version of the static frontend into the backend `cp -r frontend/build backend/static`
1. Install dependencies for the backend: `cd backend && pip3 install -r requirements.txt`
1. Start the backend: `python3 entrypoint.py`
1. Access the application by visiting https://localhost:4545/

## Building + Running via Docker

This project includes a Dockerfile that can be used to build the entire application (frontend and backend) as a single Docker container.  If running via Docker, you still need to provide access to a MongoDB instance that the application can use for storing questions and tests.  If you have the database running on the same machine as the application, you should be able to pass `--net host` to the `docker run` command to give it access to the database directly (this doesn't work on MacOS).  If the database is running on a different host or non-default port, you'll need to pass the configuration values as environment variables to the `docker run` command like `-e MONGO_PORT=39393`.

1. `docker build -t quizzing .`
2. `docker run -it -p 4545:4545 quizzing`
