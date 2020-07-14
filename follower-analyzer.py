from igramscraper.instagram import Instagram
from time import sleep
from datetime import date
from getpass import getpass
import csv
import os

username = ''
password = ''
nbFollow = 0

instagram = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

today = date.today()

followers = []
following = []
bastards = []
miskines = []
verifiedFollow = []
verifiedFollowers = []
# account = instagram.get_account(username)
# print(bcolors.OKGREEN + 'Connected to account ' + bcolors.BOLD + account.full_name + ' @' + account.username + bcolors.ENDC)

def loading():
  print('Loading...')

def login():
  username = input("Type your username: ")
  password = getpass("Type your password: ")
  nbFollow = int(input("Type the number of people you are following: "))
  instagram = Instagram()
  instagram.with_credentials(username, password, './cache/')
  try:
    instagram.login(force=False,two_step_verificator=True)
  except Exception:
    print('Incorrect credentials. Relaunch and try again.')
    return False
  sleep(2) # Delay to mimic user
  account = instagram.get_account(username)
  print(bcolors.OKGREEN + 'Connected to account ' + bcolors.BOLD + account.full_name + ' @' + account.username + bcolors.ENDC)
  print("Export date: ", today.strftime("%d/%m/%Y"))
  return True

# def get_followers():
#   sleep(1)
#   followers = instagram.get_followers(account.identifier, 400, 100, delayed=True) # Get 400 followers of 'kevin', 100 a time with random delay between requests # Delay to mimic user

# def get_following():
#   sleep(1)
#   following = instagram.get_following(account.identifier, nbFollow, 100, delayed=True)

def contains(list, filter):
  for x in list:
    if filter(x):
        return True
  return False

def show_followers(show):
  if show:
    print(bcolors.BOLD + '\nFollowers\n' + bcolors.ENDC)
    for follower in followers['accounts']:
        print(follower.username + ' - ' + follower.full_name)
    print('Total: ' + str(len(followers['accounts'])) + '\n')

def show_following(show):
  if show:
    print(bcolors.BOLD + '\nFollowing\n' + bcolors.ENDC)
    for follow in following['accounts']:
        print(follow.username + ' - ' + follow.full_name)
    print('Total: ' + str(len(following['accounts'])) + '\n')

def get_bastards():
  print(bcolors.BOLD + '\nPeople I follow that do not follow me\n' + bcolors.ENDC)
  for follow in following['accounts']:
      if contains(followers['accounts'], lambda x: x.username == follow.username) == False:
        if follow.is_verified == False:
          bastards.append(follow)
  for bastard in bastards:
      print(bastard.username + ' - ' + bastard.full_name)
  print('Total: ' + str(len(bastards)) + '\n')

def get_miskines():
  print(bcolors.BOLD + '\nPeople I do not follow that follow me\n' + bcolors.ENDC)
  for follower in followers['accounts']:
      if contains(following['accounts'], lambda x: x.username == follower.username) == False:
        miskines.append(follower)
  for miskine in miskines:
      print(miskine.username + ' - ' + miskine.full_name)
  print('Total: ' + str(len(miskines)) + '\n')

def get_verified_followed():
  print(bcolors.BOLD + '\nVerified account I follow\n' + bcolors.ENDC)
  for follow in following['accounts']:
    if follow.is_verified == True:
      verifiedFollow.append(follow)
  for verified in verifiedFollow:
    print(verified.username + ' - ' + verified.full_name)
  print('Total: ' + str(len(verifiedFollow)) + '\n')

def get_verified_followers():
  print(bcolors.BOLD + '\nVerified account that follow me\n' + bcolors.ENDC)
  for follower in followers['accounts']:
    if follower.is_verified == True:
      verifiedFollowers.append(follower)
  for verified in verifiedFollowers:
    print(verified.username + ' - ' + verified.full_name)
  print('Total: ' + str(len(verifiedFollowers)) + '\n')

def get_file_name():
  maxNb = 0
  nextName = ""
  try:
    onlyfiles = [f for f in os.listdir('./export/') if os.path.isfile(os.path.join('./export/', f))]
  except FileNotFoundError:
    if input('Export directory not existing. Create ? [y/n]:\n') == "y":
      os.mkdir('export')
      print('Export folder created')
      onlyfiles = [f for f in os.listdir('./export/') if os.path.isfile(os.path.join('./export/', f))]
    else:
      print('Export aborted')
      return ''
  for f in onlyfiles:
    if int(f.replace('.csv', '')) > maxNb:
      maxNb = int(f.replace('.csv', ''))
  maxNb = maxNb + 1
  nextName = str(maxNb) + '.csv'
  print('Export name: ' + nextName)
  return nextName

def create_export():
  filename = get_file_name()
  username = input("Type your username: ")
  password = getpass("Type your password: ")
  nbFollow = int(input("Type the number of people you are following: "))
  instagram = Instagram()
  instagram.with_credentials(username, password, './cache/')
  try:
    instagram.login(force=False,two_step_verificator=True)
  except Exception as e:
    print(e)
    print('Incorrect credentials. Relaunch and try again.')
    return False
  sleep(2) # Delay to mimic user
  account = instagram.get_account(username)
  print(bcolors.OKGREEN + 'Connected to account ' + bcolors.BOLD + account.full_name + ' @' + account.username + bcolors.ENDC)
  print("Export date: ", today.strftime("%d/%m/%Y"))
  loading()
  sleep(1)
  followers = instagram.get_followers(account.identifier, 400, 100, delayed=True) # Get 400 followers of 'kevin', 100 a time with random delay between requests # Delay to mimic user
  sleep(1)
  following = instagram.get_following(account.identifier, nbFollow, 100, delayed=True)
  if filename != '':
    with open('./export/' + filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Followers'])
        for follower in followers['accounts']:
          filewriter.writerow([follower.username, follower.full_name])
        filewriter.writerow(['Total: ' + str(len(followers['accounts']))])
        filewriter.writerow([''])
        filewriter.writerow(['Following'])
        for follow in following['accounts']:
          filewriter.writerow([follow.username, follow.full_name])
        filewriter.writerow(['Total: ' + str(len(following['accounts']))])
        filewriter.writerow([''])
        filewriter.writerow(['People I follow that do not follow me'])
        for follow in following['accounts']:
            if contains(followers['accounts'], lambda x: x.username == follow.username) == False:
              if follow.is_verified == False:
                bastards.append(follow)
        for bastard in bastards:
            filewriter.writerow([bastard.username, bastard.full_name])
        filewriter.writerow(['Total: ' + str(len(bastards))])
        filewriter.writerow([''])
        filewriter.writerow(['People I do not follow that follow me'])
        for follower in followers['accounts']:
            if contains(following['accounts'], lambda x: x.username == follower.username) == False:
              miskines.append(follower)
        for miskine in miskines:
            filewriter.writerow([miskine.username, miskine.full_name])
        filewriter.writerow(['Total: ' + str(len(miskines))])
        filewriter.writerow([''])
        filewriter.writerow(['Verified account I follow'])
        for follow in following['accounts']:
          if follow.is_verified == True:
            verifiedFollow.append(follow)
        for verified in verifiedFollow:
          filewriter.writerow([verified.username, verified.full_name])
        filewriter.writerow(['Total: ' + str(len(verifiedFollow))])
        filewriter.writerow([''])
        filewriter.writerow(['Verified account that follow me'])
        for follower in followers['accounts']:
          if follower.is_verified == True:
            verifiedFollowers.append(follower)
        for verified in verifiedFollowers:
          filewriter.writerow([verified.username, verified.full_name])
        filewriter.writerow(['Total: ' + str(len(verifiedFollowers))])
        filewriter.writerow([''])
        filewriter.writerow(['Date: ' + today.strftime("%d/%m/%Y")])
    print('Export ' + filename + ' finished')

def shell_export():
  if login():
    loading()
    sleep(1)
    followers = instagram.get_followers(account.identifier, 400, 100, delayed=True) # Get 400 followers of 'kevin', 100 a time with random delay between requests # Delay to mimic user
    show_followers(True)
    sleep(1)
    following = instagram.get_following(account.identifier, nbFollow, 100, delayed=True)
    show_following(True)
    get_bastards()
    get_miskines()
    get_verified_followed()
    get_verified_followers()
  
def main():
  if input('Would you like to export the result ? [y/n]\n') == 'y':
    create_export()
  else:
    shell_export()

main()