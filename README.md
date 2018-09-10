# tweetdelete
A command line tool that lets the user review and remove any of the tweets they've ever made. This is a solution to the Twitter API's limit of showing only the most recent 3,200 tweets.

## external-libraries
The libraries used in this project are the tweepy (for API accesses) and pyinstaller (for building) library, which can be installed using pip using
```
pip install tweepy
pip install pyinstaller
```

## outside-requirements
In order to use this application properly, there is some preliminary work to be done.

First, we need to get our keys needed to authenticate ourselves through the API. Head to the [Twitter Apps page](https://apps.twitter.com/) and apply for a developer account. Follow the directions (it doesn't matter what you name the app). Once you've created your account, you'll need to grab the authorization codes they provide. The public consumer key and secret consumer key should already be displayed on the page, but you will probably need to generate the public access key and its secret counterpart. Do **not** share these codes with anybody.

Second, we need our tweet archive, which is conveniently provided by Twitter. On Web Twitter, head to your profile icon on the upper-right corner of the screen and open the dropdown. Click on **Settings and privacy**, and navigate towards the bottom where you should see a button saying **Request your archive**. If the button says **Resend email** then you will have to wait an undefined amount of time (not known to me) before you can generate another one. Otherwise, click on **Request your archive**, which should send an e-mail containing the .csv archive to the currently registered address.

At this point you should have everything you need to run the prompt.

## how-to-use

Navigate to the directory containing the tweetdelete executable and run it.
