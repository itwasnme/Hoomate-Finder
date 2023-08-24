from django.test import TestCase
from django.test.client import RequestFactory

from django.contrib.auth.models import AnonymousUser, User
from .models import Profile
from .views import getProfileForm, profileSearch, ProfileIndexView, get_matches, home, getDetail, action

import requests, json, random, string

# Create your tests here.
class Tests(TestCase):
    
    def setUp(self):
        # Randomly generates a string of input, used to make sure that variable user inputs can pass.
        letters = string.ascii_lowercase
        choice = random.randint(1, 5)
        if choice == 1:
            letters = string.ascii_lowercase
        elif choice == 2:
            letters = string.ascii_uppercase
        elif choice == 3:
            letters = string.ascii_letters
        elif choice == 4:
            letters = string.digits
        elif choice == 5:
            letters = string.punctuation
        randomInput = ''.join(random.choice(letters) for i in range(random.randint(1, 50)))
        print("Random user input is: " + str(randomInput))
        
        # A test profile utilized to see different views based on whether the user is authenticated or not.
        self.testProfile = Profile(username='tester', name_text=randomInput, bio_text=randomInput,
            age=19, grad_year=2023, budget_lower=500, budget_upper=800, noise_level=1, gender="test profile",
            personality="Extrovert",location=randomInput,car=randomInput)

        self.testProfile2 = Profile(username='secondTestProfile', name_text='name_text is secondTestProfile', bio_text='bio_text',
            age=19, grad_year=2025, budget_lower=500, budget_upper=800, noise_level=1, gender="test profile 2",
            personality="Introvert",location='location',car='car')
        
        self.testProfile2.save()
        self.testProfile.save()

        self.testUser = User.objects.create_user(username='tester')
        self.testUser2 = User.objects.create_user(username='secondTestProfile')

        # To emulate GET and POST requests
        self.factory = RequestFactory()
    
    """ Intitial check to see if accessing pages does not return a 404. """

    def test_home_page(self):
        """ Tests to see if accessing the home page works. """
        request = self.factory.get('/')

        request.user = self.testUser

        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_creation_link(self):
        """ Tests to see if accessing the create link works. """
        request = self.factory.get('/create/')

        request.user = self.testUser

        response = getProfileForm(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_list_link(self):
        """ Tests to see if accessing the profile listing link works. """
        """ Currently not used, so this test isn't completely necessary unless we want to utilize this feature in the future. """
        request = self.factory.get('/list/')

        request.user = self.testUser

        response = ProfileIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_roommate_search_link(self):
        """ Tests to see if accessing the roommate search link works. """
        request = self.factory.get('/search/')

        request.user = self.testUser

        response = profileSearch(request)
        self.assertEqual(response.status_code, 200)

    def test_matches_link(self):
        """ Tests to see if the matches screen works. """
        request = self.factory.get('/matches/')

        request.user = self.testUser

        response = get_matches(request)
        self.assertEqual(response.status_code, 200)

    def test_detail_link(self):
        """ Tests to see if an authenticated can reach a valid profile. """
        request = self.factory.get('/')
        request.user = self.testUser
        
        # Gets the test profile link
        request = self.factory.get('/'+str(request.user.id))
        request.user = self.testUser

        # Checks to see if the randomly generated test name in the test profile is displayed in the render
        response = getDetail(request, request.user.id)
        self.assertEqual(response.status_code, 200)

    """ Checks to see if content is actually returning what is supposed to. """

    def test_home_page_content(self):
        """ Tests to see if accessing the home page returns home page content. """
        request = self.factory.get('/')

        request.user = self.testUser

        response = home(request)
        home_page_title = "<title> Hoommate Finder </title>"
        self.assertTrue(home_page_title in str(response.content))
    
    def test_profile_creation_content(self):
        """ Tests to see if the create link returns profile content if the user is authenticated. """
        request = self.factory.get('/create/')

        request.user = self.testUser

        response = getProfileForm(request)
        profile_title = "<title>Update Profile</title>"
        self.assertTrue(profile_title in str(response.content))

    def test_unauthenticated_profile_creation_content(self):
        """ Tests to see if the create link returns homepage content if the user is NOT authenticated. """
        request = self.factory.get('/create/')

        request.user = AnonymousUser()

        response = getProfileForm(request)
        profile_title = "<title> Hoommate Finder </title>"
        self.assertTrue(profile_title in str(response.content))

    def test_detail_content(self):
        """ Tests to see if an authenticated user can see a specific profile. """
        # Gets the test profile link
        request = self.factory.get('/'+str(self.testUser.id))
        request.user = self.testUser

        # Checks to see if the display name of the test profile is in the returned render
        response = getDetail(request, self.testUser.id)
        userDisplayed = Profile.objects.get(id=self.testUser.id)
        self.assertTrue(userDisplayed.name_text in str(response.content))

    def test_unauthenticated_detail_content(self):
        """ Tests to see if a user NOT authenticated (logged in) can see a specific profile. """
        request = self.factory.get('/'+str(self.testUser.id))
        request.user = AnonymousUser()
        
        # Checks to see if the display name of the test profile is NOT in the returned render
        response = getDetail(request, self.testUser.id)
        userDisplayed = Profile.objects.get(id=self.testUser.id)
        self.assertFalse(userDisplayed.name_text in str(response.content))

        # Checks to see if an unauthenticated user is returned to the home page
        profile_title = "<title> Hoommate Finder </title>"
        self.assertTrue(profile_title in str(response.content))
    
    def test_match_content(self):
        """ Tests to see if a user authenticated can see their matches (if any). """
        request = self.factory.get('/matches/')

        request.user = self.testUser

        response = get_matches(request)
        match_title = "<title>Your Matches</title>"
        self.assertTrue(match_title in str(response.content))

    def test_unauthenticated_match_content(self):
        """ Tests to see if a user NOT authenticated can see their matches (if any). """
        request = self.factory.get('/matches/')

        request.user = AnonymousUser()

        response = get_matches(request)
        match_title = "<title>Your Matches</title>"
        self.assertFalse(match_title in str(response.content))

        profile_title = "<title> Hoommate Finder </title>"
        self.assertTrue(profile_title in str(response.content))

# More tests will be added once the designs for the rest of the website have been added.

    """ Checks to see if functionality is working. """
    def test_roommate_hunt(self):
        """ Check to see if 'testProfile2' can be seen by testUser """
        request = self.factory.get('/search')
        request.user = self.testUser

        response = profileSearch(request)
        userDisplayed = 'name_text is secondTestProfile'
        self.assertTrue(userDisplayed in str(response.content))

    def test_swipe_right(self):
        """ Check to see if swiping right on 'testProfile2' from the original test profile works """
        request = self.factory.get('/action')
        request.user = self.testUser

        request.POST._mutable = True
        request.POST['username'] = Profile.objects.get(username='secondTestProfile').username
        request.POST['action'] = 'Right'
        request.POST._mutable = False

        # Response should be redirect since it's what done in the action() method
        response = action(request)
        self.assertEqual(response.status_code, 302)
    
    def test_swipe_right_from_testProfile2(self):
        """ Check to see if swiping right on 'tester' from testProfile2 works """
        request = self.factory.get('/action')
        request.user = self.testUser2

        request.POST._mutable = True
        request.POST['username'] = Profile.objects.get(username='tester').username
        request.POST['action'] = 'Right'
        request.POST._mutable = False

        # Response should be redirect since it's what done in the action() method
        response = action(request)
        self.assertEqual(response.status_code, 302)

    def test_match(self):
        """ Check to see if a match can be seen if both users swipe right on each other. """
        # tester swipes right on testUser2
        request = self.factory.get('/action')
        request.user = self.testUser

        request.POST._mutable = True
        request.POST['username'] = Profile.objects.get(username='secondTestProfile').username
        request.POST['action'] = 'Right'
        request.POST._mutable = False

        response = action(request)

        # testUser2 swipes right on tester
        request = self.factory.get('/action')
        request.user = self.testUser2

        request.POST._mutable = True
        request.POST['username'] = Profile.objects.get(username='tester').username
        request.POST['action'] = 'Right'
        request.POST._mutable = False

        response = action(request)

        # It's a match!
        request = self.factory.get('/matches')
        request.user = self.testUser

        response = get_matches(request)
        match_confirmation = "Message Now"
        self.assertTrue(match_confirmation in str(response.content))
