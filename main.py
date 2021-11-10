# Standard
import json
import random
import smtplib
import ssl
import traceback

# Local
from Logging import logger as log

random.seed()

context = ssl.create_default_context()
cfg = None
mailServerPort = 465
mailServerUrl = "smtp.gmail.com"
ownerEmail = None
players = None
playersOriginal = None
senderEmail = None
senderPassword = None
smtpSsl = None

class Player:
  def __init__(self, name, email):
    self.name = name
    self.email = email
    self.recipient = None

  def __repr__(self):
    playerJson = {}
    playerJson["name"] = self.name
    playerJson["email"] = self.email
    if self.recipient:
      playerJson["recipient"] = self.recipient.name
    return json.dumps(playerJson)

  def __lt__(self, other):
    return self.name < other.name

def main():
  global smtpSsl
  try:
    loadConfig()
    smtpSsl = smtplib.SMTP_SSL(mailServerUrl, mailServerPort, context=context)
    smtpSsl.login(senderEmail, senderPassword)
    loadPlayers()
    pairPlayers()
    sendNotifications()
  except Exception as e:
    log.error(e)
    if not smtpSsl:
      smtpSsl = smtplib.SMTP_SSL(mailServerUrl, mailServerPort, context=context)
      smtpSsl.login(senderEmail, senderPassword)
    recipientEmail = ownerEmail
    msg = '''To: {}
Subject: Felsher Family Secret Santa Script Error!

An error occurred while running the secret santa script:

{}'''.format(recipientEmail, traceback.format_exc())
    log.info("Sending email:\n{}".format(msg))
    smtpSsl.sendmail(senderEmail, recipientEmail, msg)
    raise e

def loadConfig():
  global cfg
  global ownerEmail
  global senderEmail
  global senderPassword
  cfgFilename = "cfg.json"
  log.info("Loading config: {}".format(cfgFilename))
  with open(cfgFilename) as cfgFile:
    cfg = json.load(cfgFile)
  ownerEmail = cfg["ownerEmail"]
  senderEmail = cfg["senderEmail"]
  senderPassword = cfg["senderPassword"]

def loadPlayers():
  global players
  global playersOriginal
  playersJsonFilename = "players.json"
  players = []
  log.info("Loading players: {}".format(playersJsonFilename))
  with open(playersJsonFilename) as playersJsonFile:
    playersJson = json.load(playersJsonFile)
    for playerJson in playersJson["players"]:
      players.append(Player(playerJson["name"], playerJson["email"]))
  playersOriginal = players
  log.info("Loaded players: {}".format(players))

def pairPlayers():
  random.shuffle(players)
  log.info("Shuffled players: {}".format(players))
  for playerIndex in range(len(players)):
    players[playerIndex].recipient = players[(playerIndex + 1) % len(players)]
  log.info("Paired players: {}".format(players))

def sendNotifications():
  random.shuffle(players)

  for player in players:
    msg = '''To: {}
Subject: Felsher Family Secret Santa

{},

Your Felsher Family Secret Santa recipient is: {}.

Regards,
Andrew's coding skills'''.format(player.email, player.name, player.recipient.name)
    log.info("Sending email to {} ({}):\n{}".format(player.name, player.email, msg))
    smtpSsl.sendmail(senderEmail, player.email, msg)

  players.sort()
  recipientList = ""
  for player in players:
    recipientList += "{} ({})\n".format(player.name, player.email)

  recipientEmail = ownerEmail
  msg = '''To: {}
Subject: Felsher Family Secret Santa ran successfully!

The secret santa script ran successfully and notified the following participants:

{}'''.format(recipientEmail, recipientList)
  log.info("Sending email:\n{}".format(msg))
  smtpSsl.sendmail(senderEmail, recipientEmail, msg)

main()
