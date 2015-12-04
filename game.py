# Use everything from ex37

from random import randint

has_horse = False
has_key = False
has_leaf = False
has_sword = False
has_rope = False
old_man_hint = False
door_options = []

gallops = 0

def welcome():
  print """BEGIN"""
  raw_input()
  start()

def start():
  print """
  Until today, The forest of Glorest-bay\n
  always had a magical glow.\n
  It suddenly began fading\n
  and time seemed to slow\n
  You must find out why!!!\n
  Or the forest will die!!!!\n
  """
  pickPath()

def askForHorse():
  global has_horse
  if has_horse == False:
    print "A really cute horse appears from the shadows. There's no saddle, though. Do you take the horse?"
    answer = raw_input("> ")
    if answer == "yes":
      has_horse = True
      global gallops 
      gallops = 24
      print "You mount the stallion!!!  He neighs with joy and you trot off together..."
      door_options.append('stallion')
    else: 
      print "You signal the horse away. He turns.. neighs with sadness.. and trots off alone"
  else:
    print "You are back to where you found your stallion. Shall you continue your journey together?"
    answer = raw_input("> ")
    if answer == "yes":
      print "You whisper to your horse.. I would never leave you, buddy, and trot off together"
    else: 
      print "You dismount and signal the horse away. He turns.. neighs with sadness.. and trots off alone"
      has_horse = False
      door_options.remove('stallion')

def ride():
  global has_horse
  global gallops
  if has_horse == True and gallops >= 8:
    print "GALLOP GALLOP GALLOP"
    gallops = gallops - 8
    print "You have %r gallops remaining" % gallops
  elif has_horse == True and gallops <= 8:
    print """Your stallion doesn't have enough gallops left!!\n
         You must return him to the beginning for a whole turn so he can rest!!"""
    pickPath()
  else:
    i=0
    for i in range(0,4):
      print"you've been walking a while, do you want to continue?"
      answer = raw_input("> ")
      if answer == "yes":
        print "you keep on walking...."
      else:
        print "Too bad.  Should've taken that horse"
      i = i + 1


def pickPath():
  global old_man_hint
  askForHorse()
  if not old_man_hint:
    print "You see a man.  Talk to him?"
    answer = raw_input("> ")
    if answer == "yes":
      old_man_hint = True
      print "Old man: You.. you must travel down the, still, glowwwiiieeeest of all paths.....cough cough..."
    else: 
      print "You nod towards the man and move on"
  print"""There seem to be 5 different paths ahead:
      1. A dark swampy path that may be very treachorous ahead\n
      2. A narrow and windy path with colorful autumn leaves rustling everywhere\n
      3. A wide cobble stone path with glow still emanating everywhere\n
      4. A solid red brick path lined with once breathtaking statues of knights, but now only crumbled peices remain\n
      5. A gushing river where no animals can travel!\n """
  print "Which path do you take?"
  try:
    acceptable_answer = range(1,6)
    answer = int(raw_input("> "))
    if answer not in acceptable_answer:
      raise ValueError
  except ValueError:
    print "You must choose a path from 1 to 5, before the forest dies!"
    pickPath()
  if answer == 1:
    goSwamp()
  elif answer == 2:
    goAutumn()
  elif answer == 3:
    goGlow()
  elif answer == 4:
    goBrick()
  elif answer == 5:
    goRiver()

def youWin():
  print "You win the game!  Glorest-bay is saved!"
  exit()

def goSwamp():
  print "swamp"
  print "you found the key!"
  global has_key
  has_key = True
  pickPath()

def goAutumn():
  global has_leaf
  print "There's a fork in the road.. Do you go left or right?"
  answer = raw_input("> ")
  if 'left' in answer:
    print "This leads to a dead end!!  You turn back around.."
    goAutumn()
  elif 'right' in answer and has_leaf == False:
    print "This leads to a dead end!!\n But wait... one leaf seems strange compared to the others\n"
    print "You pick the leaf up and suddenly feel it's power!  You decide to keep the leaf!"
    has_leaf = True
    door_options.append('autumn leaf')
    print "And you head back to the beginning..."
    pickPath()
  elif 'right' in answer and has_leaf == True:
    print "You take a moment to remember the power you felt from picking up the leaf...\n"
    print "And you head back to the beginning..."
    pickPath()
  else:
    print "The forest is dying!! You don't have time to explore for the fun of it!! You can only go 'left' or 'right'!"
    goAutumn()


def goGlow():
  global has_key
  global has_horse
  if has_key == False:
    print "Amidst the mellow glow and quiet wind's blow,\n a man appears milling about, short and stout.\nHe quickly gets excited after seeing you."
    print "Old man #2: We must open this door!! Someone is attacking the glow source inside! Do you have the key?!?!"
    print "You realize you do not have they key and have to turn back!!"
    pickPath()
  else:
    mapped_options = {}
    print """With the key in hand, you slowly unlock the door.\n
         There's an evil monster eating the tree!!\n
         What do you do?"""
    i=0
    # for opt in door_options:
    #   i += 1
    #   mapped_options.append(str(door_options[i-1]))
    #   print(str(i) + ') Use the ' + door_options[i])

    # answer = map(int, raw_input("> ").split(','))

    for opt in door_options:
      i += 1
      print "%r. Use the %r!!!" % (i, opt.strip("'"))
      mapped_options[i] = opt
    answer = int(raw_input('> '))

    chosen_option = mapped_options[answer]

    print chosen_option
    if 'stallion' in chosen_option:
      print """You send your stallion into the heat of battle!!  The stallion performs a finishing blow and kills the monster.\n
           But it was too much for the stallion... he neighs his last breath."""
      global has_horse
      has_horse = False
      youWin()
    if 'shiny sword' in chosen_option and has_horse == True:
      print "You confront the monster alone and duel to the death!! Your trusty sword deals the finishing blow and you kill the monster!!\n"
      youWin()
    if 'frayed rope' in chosen_option and has_horse == True:
      print """this"""
      youWin()

def goBrick():
  global has_sword
  if has_sword:
    print "You remember this is where you found the shiny sword!! Do you still want to press the buttons?"
    answer = raw_input("> ")
    if answer == "no":
      print "You make your way back to the main path"
      pickPath()
  print "You notice 5 statues each with a button.  Which button do you press?"
  try:
    answer = int(raw_input("> "))
  except ValueError:
    print "you must pick a statue from 1 - 5!!!"
    goBrick()
  if answer == randint(0,5) and not has_sword:
    print "The statue starts moving and crumbling apart!!  Finally, as the dust clears, a shiny sword emerges!!!!\n  You take the sword, obviously."
    door_options.append('shiny sword')
    has_sword = True
    print "And you head back to the beginning..."
    pickPath()
  elif answer == randint(0,5) and has_sword:
    print "The statue starts shaking again!!  What's going to happen now?!?!!?!?"
    print "Nothing happens........ "
    print "You head back to the main path"
  else:
    print "You chose the wrong option!!  The statues rotate."
    goBrick()
  pickPath()

def goRiver():
  global has_horse
  global has_rope
  print "You approach a rushing river!!"
  if has_horse == True:
    print "You can't take your horse here!!!\n  He will die!!!  You must return him!!!"
    print "You retrace your steps through the path, back to the beginning...."
    pickPath()
  else:
    print """You must cross the river to find any valuable tools on the other side\n
         There's a canoe.  Take the canoe?"""
    answer = raw_input("> ")
    if 'yes' in answer:
      print "You row the canoe to the other side of the river, safely"
    elif 'no' in answer:
      print "You swim frantically, almost drowning, to the other side of the river.  Now you're all wet."
    else:
      print "What do you want to do?"
      goRiver()
    if not has_rope:
      print "There's some frayed old rope over here.  You take the rope, just in case."
      door_options.append('frayed rope')
      has_rope = True
    print "And you head back to the beginning..."
    pickPath()

welcome()
