from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from .models import Profile, Messages, oldMessages
from .models import g_choices
from .models import p_choices
from .models import c_choices
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Action
import requests, json
from collections import OrderedDict

# Create your views here.

def home(request):
    return render(request, 'user/home.html',{})

"""
Displays the user page (which includes links to updating bio, going on the roommate hunt, etc). Redirects to home page if not logged in
"""
def get_user(request):
    if request.user.is_authenticated:
        return render(request, 'user/index.html',{"profile": Profile.objects.filter(username = request.user.username)})
    else:
        return render(request, 'user/home.html',{})

"""
Logs the current user out and redirects to the home page.
"""
def logout_view(request):
    logout(request)
    return render(request, 'user/home.html',{})

"""
Lists all completed profiles
"""
class ProfileIndexView(generic.ListView):
    template_name = 'user/profileList.html'
    context_object_name = 'latest_profile_list'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Profile.objects.order_by('-name_text')[:]

"""
Displays a potential roommate as part of the search, as well as options to swipe left and right.
"""
def profileSearch(request):
    if request.user.is_authenticated:
        actions = Action.objects.filter(firstUser=request.user.username)
        secondUsers = set()
        for action in actions:
            secondUsers.add(action.secondUser)
        profiles = Profile.objects.all()
        context = {}
        currentuser = Profile.objects.get(username=request.user.username)
        for profile in profiles:
            if profile.username == request.user.username:
                continue
            if profile.username not in secondUsers:
                #start filtering here
                if profile.age != "" and currentuser.agemin != "" and int(profile.age) < int(currentuser.agemin):
                    continue
                if profile.age != "" and currentuser.agemax != "" and int(profile.age) > int(currentuser.agemax):
                    continue
                if profile.grad_year != "" and currentuser.grad_yearmin != "" and int(profile.grad_year) < int(currentuser.grad_yearmin):
                    continue
                if profile.grad_year != "" and currentuser.grad_yearmax != "" and int(profile.grad_year) > int(currentuser.grad_yearmax):
                    continue
                if profile.budget_upper != "" and currentuser.budget_lowerfilter != "" and int(profile.budget_upper) < int(currentuser.budget_lowerfilter):
                    continue
                if profile.budget_lower != "" and currentuser.budget_upperfilter != "" and int(profile.budget_lower) > int(currentuser.budget_upperfilter):
                    continue
                if profile.noise_level != "" and currentuser.noise_levelmin != "" and int(profile.noise_level) < int(currentuser.noise_levelmin):
                    continue
                if profile.noise_level != "" and currentuser.noise_levelmax != "" and int(profile.noise_level) > int(currentuser.noise_levelmax):
                    continue
                if profile.gender != "" and currentuser.genderfilter != "" and profile.gender != currentuser.genderfilter:
                    continue
                if profile.personality != "" and currentuser.personalityfilter != "" and profile.personality != currentuser.personalityfilter:
                    continue
                if profile.car != "" and currentuser.carfilter != "" and profile.car != currentuser.carfilter:
                    continue
                context["profile"] = profile
                break
        return render(request, 'user/profileSearch.html', context)
    else:
        return render(request, 'user/home.html',{})

#Action Search
class ActionSearchView(generic.ListView):
    template_name = 'user/profileSearch.html'
    context_object_name = 'latest_profile_list'

    def get_queryset(self):
        return Action.objects.order_by('-firstUser')[:]

def action(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    other = request.POST['username']
    if(request.POST['action'] == 'Left'):
        action = Action(firstUser=username, secondUser=other, met=-1)
    else:
        action = Action(firstUser=username, secondUser=other, met=1)
    action.save()

    return HttpResponseRedirect(reverse('user:search'))


    #Takes both peoples names
    # user1 (You) and user2 (other person)
    # Puts action[user1, user2, -1(Left) or 1 (Right)] in query

    #def get_other(request):
     #   user = None
      #  other = None
       # if Profile.objects.filter(username=username).exists():
        #    action = Action()
 #   def swipe(request, username)


"""
Called when you click on some one's profile you got to see all their details
"""
# class ProfileDetailView(generic.DetailView):
def getDetail(request, prof_id,*args, **kwargs):
    if request.user.is_authenticated:
        currentProfile = Profile.objects.get(pk=prof_id)
        context={"profile":currentProfile, "gchoice":g_choices, "pchoice":p_choices, "cchoice": c_choices}
        return render(request, 'user/detail.html',context)
    else:
        return render(request, 'user/home.html',{})
    # model = Profile
    # template_name = 'user/detail.html'
    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Profile.objects.order_by('-name_text')[:]

def getProfileForm(request):
    # Makes sure that user is authenticated before allowing them to update/edit their profile
    if request.user.is_authenticated:
        # Sends the current profile with the view so the view can display information about the current profile
        context = {}
        # g_choices = (
        # ('M', 'Introvert'),
        # ('F', 'Extrovert'),
        # ('O','Other/Prefer not to say')
        # )
        # p_choices = (
        # ('I', 'Introvert'),
        # ('E', 'Extrovert'),
        # )
        # c_choices = (
        # ('Y', 'Have a car'),
        # ('N', 'Do not have a car'),
        # )
        if Profile.objects.filter(username=request.user.username).exists():
            currentProfile = Profile.objects.get(username=request.user.username)
            matches = set()
            actionsgrp1 = Action.objects.filter(firstUser=request.user.username,met=1)
            actionsgrp2 = Action.objects.filter(secondUser=request.user.username,met=1)

            for action1 in actionsgrp1:
                for action2 in actionsgrp2:
                    if action1.secondUser == action2.firstUser:
                        matches.add(Profile.objects.get(username=action1.secondUser))
            context = {"profile" : currentProfile, "matches" : matches, "gchoice":g_choices, "pchoice":p_choices, "cchoice": c_choices}
            return render(request, 'user/profile.html', context)
        else:
            context={"gchoice":g_choices, "pchoice":p_choices, "cchoice": c_choices}
            return render(request, 'user/profile.html',context)
    else:
        # The user is not authenticated and should return to the home page
        return render(request, 'user/home.html',{})

"""
Called when a user clicks the button to update/create their profile
"""
def get_profile(request):
    username = None

    # Checks to see if user is authenticated 

    if request.user.is_authenticated:
        username = request.user.username
    
    # If not then redirects back to login at home screen
    if username == None or username == '':
        return render(request, 'user/home.html',{})
    else:
        # Get information from the text fields and update the profile
        if Profile.objects.filter(username=username).exists():
            #If elses check to make sure the field isnt empty so we dont overwrite prexisting data with empty values
            existingProfile = Profile.objects.get(username=username)
            if(request.POST['name_text'] != ""):
                existingProfile.name_text = request.POST['name_text']
            if(request.POST['bio_text'] != ""):
                existingProfile.bio_text = request.POST['bio_text']
            if(request.POST['age'] != ""):
                existingProfile.age = request.POST['age']
            if(request.POST['grad_year'] != ""):
                existingProfile.grad_year = request.POST['grad_year']
            if(request.POST['budget_lower'] != ""):
                existingProfile.budget_lower=request.POST['budget_lower']
            if(request.POST['budget_upper'] != ""):
                existingProfile.budget_upper=request.POST['budget_upper']
            if(existingProfile.budget_upper and existingProfile.budget_lower and int(existingProfile.budget_upper) < int(existingProfile.budget_lower)):
                #make sure they didnt put in nonsenical input
                temp=existingProfile.budget_upper
                existingProfile.budget_upper=existingProfile.budget_lower
                existingProfile.budget_lower=temp
            if(request.POST['noise_level'] != ""):
                existingProfile.noise_level=request.POST['noise_level']
            if 'gender' in request.POST:
                existingProfile.gender=request.POST['gender']
            #if(request.POST['personality'] != ""):
            if 'personality' in request.POST:
                existingProfile.personality=request.POST['personality']
            if(request.POST['location'] != ""):
                existingProfile.location=request.POST['location']
            if 'car' in request.POST:
                existingProfile.car=request.POST['car']
            if(request.POST['agemin'] != ""):
                existingProfile.agemin = request.POST['agemin']
            if(request.POST['agemax'] != ""):
                existingProfile.agemax = request.POST['agemax']
            if(existingProfile.agemax and existingProfile.agemin and int(existingProfile.agemax) <= int(existingProfile.agemin)):
                #make sure they didnt put in nonsenical input
                temp=existingProfile.agemax
                existingProfile.agemax=existingProfile.agemin
                existingProfile.agemin=temp
            if(request.POST['grad_yearmin'] != ""):
                existingProfile.grad_yearmin = request.POST['grad_yearmin']
            if(request.POST['grad_yearmax'] != ""):
                existingProfile.grad_yearmax = request.POST['grad_yearmax']
            if(existingProfile.grad_yearmax and existingProfile.grad_yearmin and int(existingProfile.grad_yearmax) <= int(existingProfile.grad_yearmin)):
                #make sure they didnt put in nonsenical input
                temp=existingProfile.grad_yearmax
                existingProfile.grad_yearmax=existingProfile.grad_yearmin
                existingProfile.grad_yearmin=temp
            if(request.POST['budget_lowerfilter'] != ""):
                existingProfile.budget_lowerfilter = request.POST['budget_lowerfilter']
            if(request.POST['budget_upperfilter'] != ""):
                existingProfile.budget_upperfilter = request.POST['budget_upperfilter']
            if(existingProfile.budget_upperfilter and existingProfile.budget_lowerfilter and int(existingProfile.budget_upperfilter) <= int(existingProfile.budget_lowerfilter)):
                #make sure they didnt put in nonsenical input
                temp=existingProfile.budget_upperfilter
                existingProfile.budget_upperfilter=existingProfile.budget_lowerfilter
                existingProfile.budget_lowerfilter=temp
            if(request.POST['noise_levelmin'] != ""):
                existingProfile.noise_levelmin = request.POST['noise_levelmin']
            if(request.POST['noise_levelmax'] != ""):
                existingProfile.noise_levelmax = request.POST['noise_levelmax']
            if(existingProfile.noise_levelmax and existingProfile.noise_levelmin and int(existingProfile.noise_levelmax) <= int(existingProfile.noise_levelmin)):
                #make sure they didnt put in nonsenical input 
                temp=existingProfile.noise_levelmax
                existingProfile.noise_levelmax=existingProfile.noise_levelmin
                existingProfile.noise_levelmin=temp
            if 'genderfilter' in request.POST:
                existingProfile.genderfilter=request.POST['genderfilter']
            if 'personalityfilter' in request.POST:
                existingProfile.personalityfilter=request.POST['personalityfilter']
            if 'carfilter' in request.POST:
                existingProfile.carfilter=request.POST['carfilter']

            if 'profile_image' in request.FILES:
                existingProfile.profile_image = request.FILES['profile_image']
            #existingProfile.profile_image = request.POST['profile_image.url']
            existingProfile.save()
        else:
        # Or create a new one if one has been created for this user
            Submitted_Profile=Profile(username=username)
            # Submitted_Profile=Profile(username=username, name_text=request.POST['name_text'],
            #  bio_text=request.POST['bio_text'], age=request.POST['age'],grad_year=request.POST['grad_year'],
            #  budget_lower=request.POST['budget_lower'], budget_upper=request.POST['budget_upper'], 
            #  noise_level=request.POST['noise_level'], gender=request.POST['gender'], 
            #  personality=request.POST['personality'], car=request.POST['car'], location=request.POST['location'],
            #  )
            if(request.POST['name_text'] != ""):
                Submitted_Profile.name_text = request.POST['name_text']
            if(request.POST['bio_text'] != ""):
                Submitted_Profile.bio_text = request.POST['bio_text']
            if(request.POST['age'] != ""):
                Submitted_Profile.age = request.POST['age']
            if(request.POST['grad_year'] != ""):
                Submitted_Profile.grad_year = request.POST['grad_year']
            if(request.POST['budget_lower'] != ""):
                Submitted_Profile.budget_lower=request.POST['budget_lower']
            if(request.POST['budget_upper'] != ""):
                Submitted_Profile.budget_upper=request.POST['budget_upper']
            if(Submitted_Profile.budget_upper and Submitted_Profile.budget_lower and int(Submitted_Profile.budget_upper) <= int(Submitted_Profile.budget_lower)):
                #make sure they didnt put in nonsenical input
                temp=Submitted_Profile.budget_upper
                Submitted_Profile.budget_upper=Submitted_Profile.budget_lower
                Submitted_Profile.budget_lower=temp
            if(request.POST['noise_level'] != ""):
                Submitted_Profile.noise_level=request.POST['noise_level']
            if 'gender' in request.POST:
                Submitted_Profile.gender=request.POST['gender']
            if 'personality' in request.POST:
                Submitted_Profile.personality=request.POST['personality']
            if(request.POST['location'] != ""):
                Submitted_Profile.location=request.POST['location']
            if 'car' in request.POST:
                Submitted_Profile.car=request.POST['car']
            if(request.POST['agemin'] != ""):
                Submitted_Profile.agemin = request.POST['agemin']
            if(request.POST['agemax'] != ""):
                Submitted_Profile.agemax = request.POST['agemax']
            if(Submitted_Profile.agemax and Submitted_Profile.agemin and int(Submitted_Profile.agemax) <= int(Submitted_Profile.agemin)):
                #make sure they didnt put in nonsenical input
                temp=Submitted_Profile.agemax
                Submitted_Profile.agemax=Submitted_Profile.agemin
                Submitted_Profile.agemin=temp
            if(request.POST['grad_yearmin'] != ""):
                Submitted_Profile.grad_yearmin = request.POST['grad_yearmin']
            if(request.POST['grad_yearmax'] != ""):
                Submitted_Profile.grad_yearmax = request.POST['grad_yearmax']
            if(Submitted_Profile.grad_yearmax and Submitted_Profile.grad_yearmin and int(Submitted_Profile.grad_yearmax) <= int(Submitted_Profile.grad_yearmin)):
                #make sure they didnt put in nonsenical input
                temp=Submitted_Profile.grad_yearmax
                Submitted_Profile.grad_yearmax=Submitted_Profile.grad_yearmin
                Submitted_Profile.grad_yearmin=temp
            if(request.POST['budget_lowerfilter'] != ""):
                Submitted_Profile.budget_lowerfilter = request.POST['budget_lowerfilter']
            if(request.POST['budget_upperfilter'] != ""):
                Submitted_Profile.budget_upperfilter = request.POST['budget_upperfilter']
            if(Submitted_Profile.budget_upperfilter and Submitted_Profile.budget_lowerfilter and int(Submitted_Profile.budget_upperfilter) <= int(Submitted_Profile.budget_lowerfilter)):
                #make sure they didnt put in nonsenical input
                temp=Submitted_Profile.budget_upperfilter
                Submitted_Profile.budget_upperfilter=Submitted_Profile.budget_lowerfilter
                Submitted_Profile.budget_lowerfilter=temp
            if(request.POST['noise_levelmin'] != ""):
                Submitted_Profile.noise_levelmin = request.POST['noise_levelmin']
            if(request.POST['noise_levelmax'] != ""):
                Submitted_Profile.noise_levelmax = request.POST['noise_levelmax']
            if(Submitted_Profile.noise_levelmax and Submitted_Profile.noise_levelmin and int(Submitted_Profile.noise_levelmax) <= int(Submitted_Profile.noise_levelmin)):
                #make sure they didnt put in nonsenical input 
                temp=Submitted_Profile.noise_levelmax
                Submitted_Profile.noise_levelmax=Submitted_Profile.noise_levelmin
                Submitted_Profile.noise_levelmin=temp
            if 'genderfilter' in request.POST:
                Submitted_Profile.genderfilter=request.POST['genderfilter']
            if 'personalityfilter' in request.POST:
                Submitted_Profile.personalityfilter=request.POST['personalityfilter']
            if 'carfilter' in request.POST:
                Submitted_Profile.carfilter=request.POST['carfilter']

            if 'profile_image' in request.FILES:
                Submitted_Profile.profile_image = request.FILES['profile_image']
            Submitted_Profile.save()
    #Corneel changed this redirect to redirect back to the profile and show the updated display for the user's profile because
    #  on discord we decided we don't plan on using profile list
    return HttpResponseRedirect(reverse('user:newprofile'))

"""
Returns the list of matches in a matches view.
"""

def get_matches(request):
    username = None

    # Checks to see if user is authenticated 
    if request.user.is_authenticated:
        username = request.user.username
    
    # If not then redirects back to login at home screen
    if username == None or username == '':
        return render(request, 'user/home.html',{})
    else:
        matches = set()
        actionsgrp1 = Action.objects.filter(firstUser=request.user.username,met=1)
        actionsgrp2 = Action.objects.filter(secondUser=request.user.username,met=1)

        for action1 in actionsgrp1:
            for action2 in actionsgrp2:
                if action1.secondUser == action2.firstUser:
                    matches.add(Profile.objects.get(username=action1.secondUser))
        context = {"matches" : matches}
        return render(request, 'user/matches.html', context)

# The idea for a message system is based off of this reference, a comment by the user 'ancho':
# Reference: https://stackoverflow.com/questions/32687461/how-to-create-a-user-to-user-message-system-using-django
def startMessage(request, uname):
    username = None
    personToChat = uname

    # Checks to see if user is authenticated 
    if request.user.is_authenticated:
        username = request.user.username
    
    context = {"match" : personToChat}
    # If not then redirects back to login at home screen
    if (username == None or username == ''):
        return render(request, 'user/home.html',{})
    else:
        return render(request, 'user/chat.html', context)

def sendMessage(request, uname):
    print("Uname to chat:", uname)
    print("Subject:", request.POST["subject"])
    print("Message:", request.POST["message"])

    newMessage = Messages(sender=request.user.username, receiver=uname, subject=request.POST["subject"], message=request.POST["message"])
    newMessage.save()
    
    return HttpResponseRedirect(reverse('user:inbox'))

def replyMessage(request, uname, prev_msg_id):
    
    repliedMessage = Messages.objects.filter(id=prev_msg_id)
    if repliedMessage.exists():
        repliedMessage = repliedMessage[0]
    else:
        print("It does not exist. Finding the current message thread.")
        repliedMessage = oldMessages.objects.filter(id=prev_msg_id)[0]
        latestMessage_id = repliedMessage.nextMessage
        print("Is it " + str(latestMessage_id) + "?")
        latestMessage = oldMessages.objects.filter(id=repliedMessage.nextMessage)
        while latestMessage.exists():
            latestMessage_id = latestMessage[0].nextMessage
            print("Is it " + str(latestMessage_id) + "?")
            latestMessage = oldMessages.objects.filter(id=latestMessage_id)
        print("It is " + str(latestMessage_id))
        repliedMessage = Messages.objects.filter(id=latestMessage_id)[0]

    newMessage = Messages(sender=request.user.username, receiver=uname, subject=repliedMessage.subject, message=request.POST["message"], previousMessage=repliedMessage.id, messageCount=(repliedMessage.messageCount + 1), mapboxLocation=repliedMessage.mapboxLocation)
    newMessage.save()

    archivedMessage = oldMessages(
        id=repliedMessage.id,
        sender=repliedMessage.sender,
        receiver=repliedMessage.receiver,
        subject=repliedMessage.subject,
        message=repliedMessage.message,
        previousMessage=repliedMessage.previousMessage,
        messageCount=repliedMessage.messageCount,
        nextMessage=newMessage.id
    )
    archivedMessage.date = repliedMessage.date
    archivedMessage.time = repliedMessage.time

    # Remove the replied message from the messages model and put it into the archive
    archivedMessage.save()
    repliedMessage.delete()

    return HttpResponseRedirect(reverse('user:viewmessage', kwargs={'msg_id': prev_msg_id}))

def get_inbox(request):
    if not request.user.is_authenticated:
        return render(request, 'user/home.html', {})
     
    context = {
        "profile" : Profile.objects.get(username=request.user.username),
        "sent" : Messages.objects.filter(sender=request.user.username).order_by('-date'),
        "received" : Messages.objects.filter(receiver=request.user.username).order_by('-date')
    }

    # print(context["profile"])
    return render(request, 'user/inbox.html', context)

def viewMessage(request, msg_id):
    if not request.user.is_authenticated:
        return render(request, 'user/home.html', {})
    
    # Get the message we want to view. If it's an outdated message, make it point back to the current message.
    message = Messages.objects.filter(id=msg_id)
    if message.exists():
        message = message[0]
    else:
        message = oldMessages.objects.filter(id=msg_id)
        if message.exists():
            message = message[0]
        else:
            context = {
                "profile" : Profile.objects.get(username=request.user.username),
                "sent" : Messages.objects.filter(sender=request.user.username),
                "received" : Messages.objects.filter(receiver=request.user.username)
            }
            return render(request, 'user/inbox.html', context)
        latestMessage_id = message.nextMessage
        latestMessage = oldMessages.objects.filter(id=message.nextMessage)
        while latestMessage.exists():
            latestMessage_id = latestMessage[0].nextMessage
            latestMessage = oldMessages.objects.filter(id=latestMessage_id)
        message = Messages.objects.filter(id=latestMessage_id)[0]

    # If the user accessing the messages is not the sender or receiver, they should not be able to see it.
    if str(message.sender) != str(request.user) and str(message.receiver) != str(request.user):
        context = {
            "profile" : Profile.objects.get(username=request.user.username),
            "sent" : Messages.objects.filter(sender=request.user.username),
            "received" : Messages.objects.filter(receiver=request.user.username)
        }
        return render(request, 'user/inbox.html', context)

    # Backtrace all of the previous messages in this conversation through the archive table.
    previousMessages = {}
    previousMessageID = message.previousMessage
    while previousMessageID != None:
        lastMessage = oldMessages.objects.filter(id=previousMessageID)[0]
        previousMessages[lastMessage.id] = lastMessage
        previousMessageID = lastMessage.previousMessage
    
    # Print out the messages in reverse order, so the most recent is at the top
    previousMessages = OrderedDict(sorted(previousMessages.items(), reverse=True))

    isSender = False
    if message.sender != None and str(message.sender) == str(request.user):
        isSender = True
    if str(message.sender) != str(request.user):
        otherprof = Profile.objects.get(username = message.sender);
    else:
        otherprof = Profile.objects.get(username = message.receiver);

    context = {
        "message": message,
        "isSender": isSender,
        "previous": previousMessages,
        "currentprofile": Profile.objects.get(username = request.user.username),
        "otherprofile": otherprof
    }

    return render(request, 'user/message.html', context)

def clear_filter(request):
    username = request.user.username

    if Profile.objects.filter(username=username).exists():
        existingProfile = Profile.objects.get(username=username)
        existingProfile.agemin = ""
        existingProfile.agemax = ""
        existingProfile.grad_yearmin = ""
        existingProfile.grad_yearmax = ""
        existingProfile.budget_lowerfilter = ""
        existingProfile.budget_upperfilter = ""
        existingProfile.noise_levelmin = ""
        existingProfile.noise_levelmax = ""
        existingProfile.genderfilter = ""
        existingProfile.personalityfilter = ""
        existingProfile.carfilter = ""
        existingProfile.save()
    return HttpResponseRedirect(reverse('user:newprofile'))

def updateMapboxAddress(request, msg_id):
    if not request.user.is_authenticated:
            return render(request, 'user/home.html', {})
        
    # Get the message we want to view. If it's an outdated message, make it point back to the current message.
    message = Messages.objects.filter(id=msg_id)
    if message.exists():
        message = message[0]
    else:
        message = oldMessages.objects.filter(id=msg_id)[0]
        latestMessage_id = message.nextMessage
        latestMessage = oldMessages.objects.filter(id=message.nextMessage)
        while latestMessage.exists():
            latestMessage_id = latestMessage[0].nextMessage
            latestMessage = oldMessages.objects.filter(id=latestMessage_id)
        message = Messages.objects.filter(id=latestMessage_id)[0]
    message.mapboxLocation = request.POST['location']
    message.save()
    return HttpResponseRedirect(reverse('user:viewmessage', kwargs={'msg_id': msg_id}))

    
