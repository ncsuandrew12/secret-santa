# Introduction
secret-santa.py is a lightweight script to organize a Secret Santa such that not even the organizer knows who is getting gifts for whom.

# Setup & Run

Running the script is pretty simple:
1. Download the script
2. Populate the input files.
3. Run the script.

## Download the script

`git clone git@github.com:ncsuandrew12/secretsanta.git`

or

`wsget https://github.com/ncsuandrew12/secretsanta/blob/master/secret-santa.py`

## Populate the input files

The script assumes the presence of two JSON files used to configure Secret Santa: `cfg.json` and `participants.json`. These
files must necessarily contain sensitive information, and so are not included in the repo.

[Example cfg.json file](cfgExample.json)

[Example participants.json file](participantsExample.json)

## Run the script

`python3 secret-santa.py`

# Notes

The script will create a `./log` directory in the current directory and any logs produced by the script will reside
there. Some logs will also be printed to the console.

`name` and `email` fields are required for all participants. Other fields are optional.

All `cfg.json` fields are mandatory.

The script will send one email to each participant. It will also send an email describing either success or an error to
the owner as specified in the `ownerEmail` config field.

Console and log output will include information on who is assigned to whom. If running manually, avoid reading output
or redirect to `/dev/null`.