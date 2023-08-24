from django.db import models

# Create your models here.
class TestModel(models.Model):
    text = models.CharField(max_length=200)

g_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other','Other')
    )
p_choices = (
        ('Introvert', 'Introvert'),
        ('Extrovert', 'Extrovert'),
    )
c_choices = (
        ('Have a car', 'Have a car'),
        ('Do not have a car', 'Do not have a car'),
    )
class Profile(models.Model):
    username = models.CharField(max_length=100, default='')
    name_text = models.CharField(default='', max_length=100)
    bio_text = models.CharField(default='',max_length=500)
    age =  models.CharField(default='', max_length=100)
    grad_year = models.CharField(default='', max_length=100)
    budget_lower = models.CharField(default='', max_length=100)
    budget_upper = models.CharField(default='', max_length=100)
    #so technically people said location was super important to them but idk how to implement that
    #maybe people can add addresses of proporties they are interested in?
    noise_level = models.CharField(default='', max_length=100) # 1-10 deal maybe change this to radio buttons 
    
    gender = models.CharField(max_length=100, choices=g_choices, default="")
    
    personality = models.CharField(max_length=100, choices=p_choices, default="")
    location = models.CharField(default='',max_length=1000)
    
    car = models.CharField(max_length=100, choices=c_choices, default="")

    agemin = models.CharField(default='', max_length=100)
    agemax = models.CharField(default='', max_length=100)
    grad_yearmin = models.CharField(default='', max_length=100)
    grad_yearmax = models.CharField(default='', max_length=100)

    budget_lowerfilter = models.CharField(default='', max_length=100)
    budget_upperfilter = models.CharField(default='', max_length=100)
    noise_levelmin = models.CharField(default='', max_length=100) # 1-10 deal maybe change this to radio buttons 
    noise_levelmax = models.CharField(default='', max_length=100) # 1-10 deal maybe change this to radio buttons 
    genderfilter = models.CharField(max_length=100, choices=g_choices, default="")
    personalityfilter = models.CharField(max_length=100, choices=p_choices, default="")
    carfilter = models.CharField(max_length=100, choices=c_choices, default="")

    profile_image = models.ImageField(null = True, blank = True, upload_to= "images/")
    
    def __str__(self):
        return "\n" + self.username + "\n" + self.name_text + "\n" + self.bio_text +"\n" + self.budget_lower +"\n" + self.budget_upper +"\n"+ self.noise_level +"\n"+ self.gender +"\n" + self.personality +"\n"+ self.location +"\n"+ self.car +"\n"


# Model for actions
class Action(models.Model):
    # Takes in the first name
    # Takes in the second name
    # Takes in whether or not they've been checked

    #firstUser = models.ForeignKey(Profile, on_delete = models.CASCADE)
    firstUser = models.CharField(max_length=100, default='')
    secondUser = models.CharField(max_length=100, default='')
    met = models.IntegerField(default = 0)


    def __str__(self):
       return "First: " + self.firstUser + " Second: " + self.secondUser + " Met: " + str(self.met)

# Model for Match Links (i.e. both users swipe right on each other and want to chat via GroupMe)
class MatchLink(models.Model):
    firstUser = models.CharField(max_length=100, default='')
    secondUser = models.CharField(max_length=100, default='')
    url = models.CharField(max_length=300)

    def __str(self):
        return "First: " + self.firstUser + " Second: " + self.secondUser + " GroupMe: " + self.url

""" Contains all of the messages a person has not replied to. """
class Messages(models.Model):
    sender = models.CharField(max_length=100, default='')
    receiver = models.CharField(max_length=100, default='')
    subject = models.CharField(max_length=200, default='')
    message = models.CharField(max_length=1000, default='')
    date = models.DateField(auto_now=False, auto_now_add=True)
    time = models.TimeField(auto_now=False, auto_now_add=True)
    previousMessage = models.IntegerField(default=None, null=True)
    messageCount = models.IntegerField(default=0)
    mapboxLocation = models.CharField(max_length=500, default='')

""" Messages that have been replied to, not displayed in inbox since its a part of a conversation """
""" All messages can in a conversation can be viewed by following the previousMessage until it is null """
class oldMessages(models.Model):
    sender = models.CharField(max_length=100, default='')
    receiver = models.CharField(max_length=100, default='')
    subject = models.CharField(max_length=200, default='')
    message = models.CharField(max_length=1000, default='')
    date = models.DateField()
    time = models.TimeField()
    previousMessage = models.IntegerField(default=None, null=True)
    nextMessage = models.IntegerField(default=None, null=True) 
    messageCount = models.IntegerField(default=0)
