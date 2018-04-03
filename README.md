# Quizzing Application Project

## Reference

* [AMC Command Line Reference](https://www.auto-multiple-choice.net/auto-multiple-choice.en/commands.shtml)
* [AMC Command Line Usage Guide](https://project.auto-multiple-choice.net/projects/auto-multiple-choice/wiki/Using_AMC_in_command_line_only)

## Installation

1. Install Python3 and Node.JS version 8.5.0 or higher
1. Make sure you have the `auto-multiple-choice` command line installed on your machine as well as `texlive-fonts-recommended`
1. Install dependencies for the frontend: `cd frontend && yarn`
1. Build a static version of the frotend: `yarn build`
1. Copy a version of the static frontend into the backend `cp -r frontend/build backend/static`
1. Install dependencies for the backend: `cd backend && pip3 install -r requirements.txt`
1. Start the backend: `python3 entrypoint.py`
