# wynnUtilities
## What is this?
wynnUtilities is a collection of scripts that use the wynncraft's api for obtaining certain thing.
## Features
- Stalker<br>
    Useful for checking what everyone is doing on wynncraft, in particular for tracking hunted people
- Checker<br>
    Want to do your prof without hunters killing you? Use this script for getting notified when a possible hunter join your server.
- Crafter<br>
    Find the perfect crafted item of your wishes
- Locator<br>
    Do you want private lootrun but you dont have friends?! Steal your friends lootrun with this feature
## How to use this?
- Install python 3.9
- pip install requirements.txt
- run main.py
## Is this bannable?
No, this program just use the wynncraft public api. So, nothing bannable.
## How to configure this?
Configuring checker and locator it's not hard, the problem begin when we talk about stalker.<br>
I suggest to leave the first 7 options as default, except for the webhooks.<br>
The filters are the hardest part to configurate and usually it take 3-4 hours to configure it. I'm not gonna give you one that is completed so, you need to input your data.<br>
For doing so you need to understand how wynnStalker works.<br>
Since when wynncraft removed chest from the api, every bot for lootrunning had to change drastically how it operates with what it has.<br>
The only way for detecting a lootrunner is by using blocksWalked but, there are lots of problems when we do this.<br>
First of all, everyone walks, unless you are afk. But everyone walks, in particular lootrunners. Lootrunners walks a lot so, you have to find a point where we can say for sure someone is a lootrunner.<br>
For getting this really important number you have to test a lot. A little help, [click this](https://api.wynncraft.com/v2/player/NoCatsNoLife/stats)<br>
Take in consideration that, blocksWalked is the buggiest thing in the whole api. How wynncraft calculate blocksWalked is actually a mistery for most people, me included.<br>
You have to configure 1 global variable, and then 5 variables for each class.<br>
The global variable is "max", why would you want to cap the max blocks walked? Because, sometimes wynncraft give milions of blocks walked randomly for no apparent reason.<br>
For each class you have to configure:
- toCheck, if you want that class to be considerate as a lootrunner
- lowStart is a value where, after this we considerate everything low (until cork). Considerate low as a gray area where we dont know if someone is lootrunning or not
- cork is the end of low, and after that we start considerating people as they have lootrunned cork.
- Cotl or Rodo or Sky (And i forgot se lmao) is the upperlimit of cork and the start of when we think that he has lootrunner one of these 3 options
- Cotl and Rodo and Sky or UnLvl is where, after this we are sure that someone has looted a fullworld, or unlvl.<br>
Do lots of test or, try to understand my configuration by looking at necron bot or aeq bot.