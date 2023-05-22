# Auto Trigger TeamCity Test Cases based on Microservices

This Python script automates the triggering of test cases in TeamCity based on changes in microservices in a Bitbucket repository. It reads the pull requests in Bitbucket, triggers builds in TeamCity, and comments in the Bitbucket pull request. Please note that this code requires a `Regression.json` file to work.

## Prerequisites

- Python 3.x
- Access to a Bitbucket repository
- Access to a TeamCity instance

## Setup

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies by running: `pip install requests`.
3. Replace the placeholders in the script with your Bitbucket and TeamCity credentials.

## Usage 

1. Open the script file in a Python editor or IDE.
2. Modify the `components` list to include the names of your microservices.
3. Run the script by executing: `python script.py` or by running it within your preferred Python environment.

## Functionality

The script performs the following steps:

1. Retrieves the pull request number from Bitbucket.
2. Identifies the target branches and upgrades for different branches.
3. Determines the microservices that have changed in the pull request.
4. Checks the running and queued builds in TeamCity.
5. Checks for running regressions in TeamCity.
6. Loads regression data from a `Regressions.json` file.
7. Determines the test cases to run based on the changed microservices and regression data.
8. Triggers the test cases in TeamCity for the relevant regressions.
9. Posts a comment in the Bitbucket pull request with the test case information.
10. Skips regression if the target branch is not one of the ongoing release branches.

Please note that the script assumes the presence of a `Regressions.json` file, which should contain the necessary regression data.

## License

This project is licensed under the [MIT License](LICENSE).
