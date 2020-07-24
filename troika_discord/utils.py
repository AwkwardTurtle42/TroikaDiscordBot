'''A place for useful utility functions'''
import random

def roll_2d6():
    '''Rolls 2d6. Returns first die, second die, total of both die'''
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1, die2, die1 + die2


def roll_d66():
    '''Rolls a d66. Returns a single value'''
    return random.randint(1,6)*10 + random.randint(1,6)


OOPS_TABLE = {
    11: "There is a flash followed by a shriek — the wizard is now a pig.",
    12: "Twenty-five years of the wizard’s life drop away in an instant, possibly making them a very small child. If the wizard is younger than twenty-five they disappear into cosmic pre-birth.",
    13: "A shoal of herring and the water they previously swam in appear above the wizard, soaking everyone.",
    14: "The wizard no longer speaks any known tongue, instead favouring a slightly unpleasant language made up of shrieks and mumbles.",
    15: "The most feared of adolescent academy curses: hiccups! Until dispelled the wizard suffers a -4 penalty to casting.",
    16: "The wizard grows a beautiful tail. If removed it doesn’t grow back.",
    21: "All currency in the wizard’s possession turns into beautiful butterflies that flap off into the sky.",
    22: "A very surprised orc appears.",
    23: "The wizard catches the Red Eye Curse. Whenever they open their eyes fire shoots out at random as per Fire Bolt.",
    24: "All shoes in the vicinity catch fire.",
    25: "The wizard grows a small pair of horns.",
    26: 'All of the wizard’s body hair falls out with an audible “fuff!”',
    31: "All Weapons in the vicinity turn into flowers.",
    32: "The wizard’s old face melts off and reveals a handsome new one.",
    33: "The wizard disappears in a puff of smoke, never to be seen again.",
    34: "The wizard’s hands find a mind of their own and take a severe disliking to the tyranny of control. They set about choking the wizard, only to lapse back into servitude as soon as they pass out.",
    35: "An overflow of plasmic fluid rushes into the wizard’s head which expands to the size of a pumpkin. If the wizard is struck for 5+ Damage in one go they must Test their Luck or their head explodes, killing them and dealing 2d6 Damage to anyone standing nearby.",
    36: "A sickness overcomes the wizard, causing them to cough up a thick black fluid. The fluid flows away as though in a hurry to be somewhere. The wizard will soon hear rumours and suffer accusations due to the workings of a sinister doppelgänger.",
    41: "Everyone in the vicinity turns into a pig except the wizard.",
    42: "All animals in the vicinity are brought back to life. This includes Provisions and leather, which will crawl and flap about blindly.",
    43: "All vegetation within a mile withers and dies.",
    44: "A pool of colour opens up under the wizard, sucking them and any other unlucky nearby souls into its depths. They will be whisked off to a random sphere of existence.",
    45: "All exposed liquid within 12 metres turns into curdling milk.",
    46: "A random spectator’s bones mysteriously disappear. Even more mysteriously, they don’t seem overly put out by it. They can’t fight or cast Spells and can only very slowly ooze about as a gelatinous blob of flesh, but they’re generally unphased. After 1d6 hours the bones pop back into place from wherever they went.",
    51: "An inanimate object in the wizard’s possession gains sentience and a voice. Its attitude is up to the GM to decide.",
    52: "A portal is opened to a paradigmatic battleground, allowing an angelic or demonic figure to pop through.",
    53: "The wizard flies off in a random direction at great speed, landing 50 metres away (or falling back down to earth, as it may be).",
    54: "The wizard suffers a coughing fit for 1d6 Turns after which 1d6 gremlins tumble out of their mouth and start biting people’s faces.",
    55: "The wizard instantly grows an enormous shaggy beard. It tumbles down to the floor and gets in the way. The wizard suffers a -2 penalty to everything until they tame that magnificent beast.",
    56: "The wizard becomes 20 years old. Today is their new birthday and they will feel terrible if no one notices.",
    61: "A calm and healthy pig appears in place of the Spell.",
    62: "The wizard’s teeth all fall out. The sudden loss causes them to suffer a -4 penalty to casting. After an hour a fresh set grows in.",
    63: "A different, random Spell goes off, directed at the same target.",
    64: "The wizard is cursed with curses. They are unable to speak without swearing and are unable to cast magic for 1d6 hours.",
    65: "The wizard sneezes mightily, knocking over all in front of them and dealing 1d6 Damage unless they successfully Test their Luck.",
    66: "The Spell being cast won’t stop. It goes completely haywire, out of control, firing off madly until the wizard is subdued."
}

def roll_oops():
    '''Rolls a d66 and looks up if it matches something on the oops table. Returns roll and consequence (or None)'''
    roll = roll_d66()
    return roll, OOPS_TABLE.get(roll, None)
