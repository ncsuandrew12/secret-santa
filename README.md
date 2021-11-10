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

Example `cfg.json` file:

```
{
  "description": "Emond's Field Secret Santa",
  "ownerEmail": "mayor+secretsanta@emondsfield.gov",
  "senderEmail": "bela+secret-santa@gmail.com",
  "senderPassword": "",
  "mailServerUrl": "smtp.gmail.com",
  "mailServerPort": 465
}
```

Example `participants.json` file:

```
{
  "particpants": [
    {
      "name": "Rand al'Thor",
      "email": "shepherd23@emondsfield.com",
      "cc": [
        "dragon@blacktower.org",
        "dragon@tear.gov",
        "dragon@cairhien.gov",
        "king@illian.gov",
        "caracarn@rhuidean.net",
        "coramoor@athaanmiere.net" ]
      "wishlists": [
        {
          "description": "list1",
          "link": "https://www.amazon.com/hz/wishlist/ls/DR8MJQ8BXAA3L"
        }, {
          "description": "list2",
          "link": "https://docs.google.com/document/d/18T_IgetKOsvNRYpjI1VnbhWssNJ4TP-lFPKSxQ/view"
        },
      ]
    }, {
      "name": "Tam al'Thor",
      "email": "prodigal@emondsfield.com",
      "cc": [ "tam.althor@illian.mil" ]
    }, {
      "name": "Bran al'Vere",
      "email": "mayor@emondsfield.gov",
      "cc": [ "bran@winespring.com" ]
    }, {
      "name": "Egwene al'Vere",
      "email": "amyrlin@tarvalon.gov",
      "cc": [ "men.are.woolheads@emondsfield.com" ]
    }, {
      "name": "Haral Luhhan",
      "email": "blacksmith@emondsfield.com"
    }, {
      "name": "Perrin Aybara",
      "email": "blacksmith2@emondsfield.com"
    }, {
      "name": "Alsbet Luhhan",
      "email": "blacksmith.wrangler@emondsfield.com"
    }, {
      "name": "Matrim Cauthon",
      "email": "gambler@band.mil",
      "cc": [ "it.wasnt.me@emondsfield.com" ]
    }, {
      "name": "Abell Cauthon",
      "email": "im.a.flaming.good.father.you.flaming.woolheads@boycottwotshow.com",
      "cc": [ "archer2@emondsfield.com" ]
    }, {
      "name": "Padan Fain",
      "email": "padan.fain@peddlers.org"
      "bcc": [ "wormwood@mashadar.net", "padan.fain@shadow.org" ]
    }, {
      "name": "Cenn Buie",
      "email": "thatcher@emondsfield.com"
    }, {
      "name": "El'Nynaeve ti al'Meara Mandragoran",
      "email": "queen@malkier.gov",
      "cc": [ "nyneave.almeara@tarvalon.gov", "wisdom@emondsfield.gov", "braidtugger@emondsfield.com" ]
    }, {
      "name": "Al'Lan Mandragoran",
      "email": "king@malkier.gov",
      "cc": [ "lan.mandragoran@tarvalon.gov", "lan.mandragoran@shienar.com" ]
    }, {
      "name": "Moiraine Merrilin",
      "email": "moiraine.damodred@tarvalon.gov",
      "cc": [ "bluestone@cairhien.com" ]
    }, {
      "name": "Thomdril Merrilin",
      "email": "thom.merrilin@tarvalon.gov",
      "cc": [ "thom.merrilin@gleemen.org", "court.bard@andor.gov" ]
    }, {
      "name": "Faile Aybara",
      "email": "lady@tworivers.gov",
      "cc": [ "faile.aybara@emondsfield.com", "zarene.bashere@saldaea.com", "mandarb@hornhunter.org" ]
    }
  ]
}
```

## Run the script

`python3 secret-santa.py`

# Notes

The script will create a `./log` directory in the current directory and any logs produced by the script will reside
there. Some logs will also be printed to the console.

`name` and `email` fields are required for all participants. Other fields are optional.

All `cfg.json` fields are mandatory.

The script will send one email to each participant. It will also send an email describing either success or an error to
the owner as specified in the `ownerEmail` config field.