
# project-a-21: Hoommate Finder

The Hoommate finder is a roommate finding service that seeks to turn Hoos into Roommates. Users are greeted with a home page that explains the concept of swiping and then will sign into the app via google account API integration. 

## Profile Creation and Hoommate Filtering
Once signed in, a user will create their profile and fill out their profile details as well as upload an image if they so desire (or stick with the default Rotunda picture). All information they input will be displayed on the left side of the page so they know what information future matches will be able to see. Additionally on this page, the user has the option to customize the filter for when they search for other profiles. Filters can be cleared if the user has a trouble finding a match with thier current filters, and all filters chosen will be displayed on the left side of the page. The filters will only prevent users that violate the filters from appearing on the search hunt (users with no trait listed will still appear on the hunt even if a filter for that specific trait is selected). Once the user has filled their information and filters out (they can come back and edit at any time), they can move forward with a Hoommate search hunt.

## The Hoommate Searching Process: Swiping

The Hoommate search hunt will display all profiles that pass all the user's filter settings one by one. Each displayed profile will display the other's user's inputted information and two buttons, an "X" to not match with the person and a checkmark to potentially match with the displayed profile. If and only if the other user also hits the checkmark button when the current user's profile is displayed, the two will be matched. 

## Matching and Messaging with other Hoommates
When the user navigates to the thier match page (either by searching through everyone in the hunt or hitting the home button at any point during the hunt), they will see the list of all their matches, showing each person's name, age, location preference, and a button to start a new chat. Upon clicking this button, the user will title the interaction and send a message, causing the message to appear in the other user's inbox. Users can see the lists of all chats with other users divided into an inbox and outbox.

In the chat window between two users, each user will see all the message history in the chat and an option to write another message. **Note that the message loading is static** - it acts more as a mailbox than a live chat, and  messages from the person you are chatting with will not be updated until the page is refreshed or an action is performed.

## Sharing Locations with Hoommates via the Mapbox API
Additionally, there is a Mapbox API integration on the screen and address box. Clicking any location inside the Mapbox will provide a pop up of that location's address, as well as a search bar inside the Mapbox window with the option to search up a specific address. Additionally, above the Mapbox window is an input field where users can share addresses. The address input into this field will be displayed on the Mapbox window for both users in the chat. If the input given is not a valid address, then the mapbox will try to autocomplete the false address and will give a location that contains the word inputted. If the address completely fails the search, then the mapbox will center at the lawn.
