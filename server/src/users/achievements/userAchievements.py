from rippleAchievements.signals import achievement_unlocked

def ach_earned(sender, user, achievement, *args, **kwargs):
        print(sender)
        print(user)
        print(achievement.key)

achievement_unlocked.connect(ach_earned)



class UsernameAchievement(object):
    name = "Username achivement"
    key = "username"
    description = "Handles when a user changes its username"
    bonus = 15.0
    def evaluate(self, user, *args, **kwargs):
        if 1 != 2:
            return True
        else:
            return False
