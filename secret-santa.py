import json
import logging
import random
import os
import smtplib
import ssl
import sys
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler

context = ssl.create_default_context()
description = None
log = None
mailServerPort = None
mailServerUrl = None
ownerEmail = None
participants = None
senderEmail = None
senderPassword = None
smtpSsl = None

def main():
  global log
  global smtpSsl

  random.seed()

  log = SetupLogger("secret-santa")

  try:
    loadConfig()
    setupSmtp()
    loadParticipants()
    pairParticipants()
    sendNotifications()
  except Exception as e:
    log.error(e)
    if not smtpSsl:
      setupSmtp()
    recipientEmail = ownerEmail
    msg = '''To: {}
Subject: {} script error!

An error occurred while running the secret santa script:

{}'''.format(recipientEmail, description, traceback.format_exc())
    log.info("Sending email:\n%s", msg)
    smtpSsl.sendmail(senderEmail, recipientEmail, msg, mail_options=['SMTPUTF8'])
    raise e

def loadConfig():
  global description
  global mailServerPort
  global mailServerUrl
  global ownerEmail
  global senderEmail
  global senderPassword

  cfgFilename = "cfg.json"
  log.info("Loading config: %s", cfgFilename)
  with open(cfgFilename) as cfgFile:
    cfg = json.load(cfgFile)
  description = cfg["description"]
  ownerEmail = cfg["ownerEmail"]
  senderEmail = cfg["senderEmail"]
  senderPassword = cfg["senderPassword"]
  mailServerPort = cfg["mailServerPort"]
  mailServerUrl = cfg["mailServerUrl"]

def setupSmtp():
  global smtpSsl

  smtpSsl = smtplib.SMTP_SSL(mailServerUrl, mailServerPort, context=context)
  smtpSsl.login(senderEmail, senderPassword)

def loadParticipants():
  global participants
  participantsJsonFilename = "participants.json"
  participants = []
  log.info("Loading participants: {}".format(participantsJsonFilename))
  with open(participantsJsonFilename) as participantsJsonFile:
    participantsJson = json.load(participantsJsonFile)
    for participantJson in participantsJson["participants"]:
      participants.append(Participant(participantJson))
  log.info("Loaded participants: %s", participants)

def pairParticipants():
  random.shuffle(participants)
  log.info("Shuffled participants: %s", participants)
  for participantIndex in range(len(participants)):
    participants[participantIndex].recipient = participants[(participantIndex + 1) % len(participants)]
  log.info("Paired participants: %s", participants)

def sendNotifications():
  random.shuffle(participants)

  for participant in participants:
    wishlistStrHtml = ""
    wishlistStrText = ""
    if participant.recipient.wishlists:
      wishlistStrHtml = "<p>{}'s wishlist(s):</p><ol>".format(participant.recipient.name)
      wishlistStrText = "\n\n{}'s wishlist(s):\n".format(participant.recipient.name)
      wishlistNum = 1
      for wishlist in participant.recipient.wishlists:
        wishlistStrHtml += "<li><a href=\"{}\">{}</a></li>".format(wishlist.link, wishlist.description)
        wishlistStrText += "{}. {}: {}\n".format(wishlistNum, wishlist.description, wishlist.link)
        wishlistNum += 1
      wishlistStrHtml += "</ol>"

    recipients = [ participant.email ]

    msg = MIMEMultipart('alternative')
    msg['To'] = participant.email
    msg['From'] = senderEmail
    if participant.cc:
      ccs = ",".join(participant.cc)
      recipients += participant.cc
      msg['CC'] = ccs
    if participant.bcc:
      bccs = ",".join(participant.bcc) # FIXME
      recipients += participant.bcc
      msg['BCC'] = bccs
    msg['Subject'] = description

    msgText = '''{},

Your {} recipient is: {}.{}'''.format(
      participant.name,
      description,
      participant.recipient.name,
      wishlistStrText)

    msgHtml = '''<html><head></head><body><p>{},<br />
<br />
Your {} recipient is: {}.</p>
{}</body></html>'''.format(
      participant.name,
      description,
      participant.recipient.name,
      wishlistStrHtml)

    msg.attach(MIMEText(msgText, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    log.info("Sending email to %s (%s)", participant.name, ",".join(recipients))
    smtpSsl.sendmail(senderEmail, recipients, msg.as_string(), mail_options=['SMTPUTF8'])

  participants.sort()
  recipientList = ""
  for participant in participants:
    recipientList += "{} ({})\n".format(participant.name, participant.email)

  recipientEmail = ownerEmail
  msg = '''To: {}
Subject: {} ran successfully!

The secret santa script ran successfully and notified the following participants:

{}'''.format(recipientEmail, description, recipientList)
  log.info("Sending email:\n%s", msg)
  smtpSsl.sendmail(senderEmail, recipientEmail, msg, mail_options=['SMTPUTF8'])

class Participant:
  def __init__(self, rjson):
    self.name = rjson["name"]
    self.email = rjson["email"]
    self.cc = None
    self.bcc = None
    self.wishlists = None
    self.recipient = None

    if "cc" in rjson:
      self.cc = rjson["cc"]
    if "bcc" in rjson:
      self.bcc = rjson["bcc"]
    if "wishlists" in rjson:
      self.wishlists = []
      for wishlistJson in rjson["wishlists"]:
        self.wishlists.append(Wishlist(wishlistJson))

  def __repr__(self):
    rjson = {}
    rjson["name"] = self.name
    rjson["email"] = self.email
    if self.cc:
      rjson["cc"] = self.cc
    if self.bcc:
      rjson["bcc"] = self.bcc
    if self.wishlists:
      rjson["wishlists"] = str(self.wishlists)
    if self.recipient:
      rjson["recipient"] = self.recipient.name
    return json.dumps(rjson)

  def __lt__(self, other):
    return self.name < other.name

class Wishlist:
  def __init__(self, json):
    self.description = json["description"]
    self.link = json["link"]

  def __repr__(self):
    rjson = {}
    rjson["name"] = self.description
    rjson["link"] = self.link
    return json.dumps(rjson)

class MaxLogLevelFilter(logging.Filter):
  def __init__(self, logLevel):
    self.logLevel = logLevel
  def filter(self, record):
    return record.levelno <= self.logLevel
  logLevel = logging.DEBUG

class Formatter(logging.Formatter):
  def format(self, record):
    record.timeZone = "EST"
    record.levelnameSuffix = (" " * (len("CRITICAL") - len(record.levelname)))
    return logging.Formatter.format(self, record)

def SetupLogger(title):
  logDir = "./log/{}".format(title)
  if not os.path.exists(logDir):
    print("Making logDir: " + logDir)
    os.makedirs(logDir)

  logger = logging.getLogger(title)
  # logger.setLevel(logging.DEBUG)
  formatter = Formatter(
    fmt="%(asctime)s %(timeZone)s %(processName)s:%(threadName)s %(levelname)s:%(levelnameSuffix)s %(pathname)s:%(lineno)d(%(funcName)s) %(message)s",
    datefmt=None)
  fileHandler = RotatingFileHandler(
    filename="{}/log.log".format(logDir),
    maxBytes=5 * 1024 * 1024, # 5MB
    backupCount=9,
    delay=True)

  fileHandler.setFormatter(formatter)

  stdoutHandler = logging.StreamHandler(stream=sys.stdout)
  stdoutHandler.setFormatter(formatter)
  stderrHandler = logging.StreamHandler(stream=sys.stderr)
  stderrHandler.setFormatter(formatter)

  logger.addHandler(fileHandler)
  logger.addHandler(stdoutHandler)
  logger.addHandler(stderrHandler)

  logging.getLogger().setLevel(logging.NOTSET)

  stdoutHandler.setLevel(logging.INFO)
  stdoutHandler.addFilter(MaxLogLevelFilter(logging.WARNING))
  stderrHandler.setLevel(logging.ERROR)

  return logger

main()
