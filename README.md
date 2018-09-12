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

Navigate to the directory containing the tweetdelete executable and run it. You should be greeted with this message:
```
welcome to tweetdelete, a command line tool that lets you find and mass delete even the oldest tweets from your account. to start, input '$ help' to the console
$ 
```
As the opening prompt states, inputting ```$ help``` will present you with a list of options. Here are some of them.
```
$ setpath
	-[path]	set path of tweet archive
$ curpath
	outputs the current path of the tweet archive
$ readcsv
	read in the csv file at the given path
$ auth
	authenticate using supplied keys (see $ edit for details)
$ edit
	-ck		edit consumer_key
		-[k] - consumer_key value
	-cs		edit consumer_secret
		-[k] - consumer_secret value
	-ak		edit access_key
		-[k] - access_key value
	-as		edit access_secret
		-[k] - access_secret value
```
The first thing we will want to do here is configure our ```archive_path``` to point to wherever our .csv is stored so that we can load it.
```
$ setpath /path/to/tweets.csv ↵
set path to archive
```
Now that we have our ```archive_path``` set up, we simply read in the .csv file using
```
$ readcsv
```
If all went well, the following will have been outputted to the console:
```
$ readcsv ↵
csv successfully read
filled in tweet ids
filled in tweet->id and id->tweet map
```
Next we will want to set up our authentication keys. The commands list tells us that ```edit -ck``` will help us set up our first key. So we input as follows:
```
$ edit -ck <key> ↵
changed consumer_key to <key>
```
Repeat this for the remaining three keys.
```
$ edit -cs <key> ↵
changed consumer_secret to <key>
$ edit -ak <key> ↵
changed access_key to <key>
$ edit -as <key> ↵
changed access_secret to <key>
```
Once the keys are set up, authenticate them.
```
$ auth ↵
authenticating
authenticated as @<your-handle>
```
From here, you can choose to list out your tweets. You have many options on how to do so, including listing by month and year, and whether it was a retweet or in respnse to someone. For example, to list all tweets from February of 2014, do:
```
$ list -ym 2014-02
```
which will output all the tweets in ```tweetid, tweetdate, tweetcontents``` format, like so:
```
$ list -ym 2014-02 ↵
437767003848572928 2014-02-24 i'm an example tweet!
435908529396785152 2014-02-24 i'm another example tweet!
```
You get the point. But if you simply want to list all of the tweets, do:
```
$ list -a
```
There's more for listing methods, simply call ```$ help``` for a full list. We will now move on to marking tweets for deletion.

To do that, use the ```$ mark``` function and add extra arguments to customize the selection. Many of the arguments used in listing tweets will also work for marking them. Arguments such as ```-yw```, ```-rt```, and ```-h``` are common among marking and listing. Note that as a safeguard, you cannot use the ```-a``` argument when marking tweets for deletion. When you do mark tweets for deletion, such as with
```
$ mark -rt GuyFieri
```
which should output something like
```
$ mark -rt GuyFieri ↵
marked 4 tweets
```
This will mark all retweets of @GuyFieri for deletion. There are many other options as well. But if you want to preserve a tweet that has been marked (see all marked tweets with ```$ list -m```), then simply ```clear``` it from the list using ```$ clear -i <tweetid>```. You can also clear the list entirely (this will **NOT** delete them) using ```$ clear -a```.

If you are satisfied with what is marked for deletion and want to proceed with deleting the tweets off your account, simply input ```$ nuke```. This will begin going through all the marked tweets and remove them from your account. This process may take a while depending on how many tweets you have marked. If done properly, then ```$ nuke``` should output
```
$ nuke ↵
4 tweets deleted
list of marked tweets cleared
```

## license
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/rilakkyuma/tweetdelete/blob/master/LICENSE) file for details
