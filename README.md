
##Fireside internet radio

created by: Brad Shepard  2014

[Fireside Internet Radio](www.firesideinternetradio.com)

Fireside Internet Radio is a project to provide personalized, streaming content to elderly patients or all people who may have difficulty using commercial media players.  Instructions are provided at www.instructables.com/id/Fireside-Internet-Radio-Player-for-Elderly-Users-b/ for how to build a headless 'radio' receiver based on Raspberry Pi.  The python code in this repository can be loaded onto the PI's sd card.

I hope you can use this code as a starting point to customize a content stream for your patient or loved one.  

Basic code function:

A) Internet radio streaming:

*Caregivers select a list of internet streaming channels (radio, books, news, etc.) and maintain the list on a Google Drive spreadsheet.
*The player simply downloads these channel addresses and switches to these selected channels with each press of the player's headset button.
*The advantage is that caregivers can select and maintain this list remotely, personalizing the content stream for the user.

B) Time, weather, personal information:

*In addition to streaming channels, the player will provide the time, weather, or other personal information at designated times (startup, shutdown, time interval, etc.)
*Uses Google Speech API (text to speech), Wundeground API (weather)
*Personal information can be added directly to the code...for example, patients with Alzheimers may need to hear a list of family names, relationships, etc. As another example, a list of family birthdays maintained on the Google drive spreasheet could be referenced.

C) Twitter (optional)
*By setting up a Twitter account for the user, tweeted messages can be read at a set frequency.
*For example, I set up a Twitter account for my grandmother (she has no idea).  New tweets are read when the player is turned on.  It is a great way for family and friends to send quick updates.


I would love to see social connectivity features, like Twitter capability, improved.  Social connection is especially important for the elderly.  If you add features, please share!

Also, if you build a player, please let me know:  brad@firesideinternetradio.com

