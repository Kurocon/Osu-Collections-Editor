OCE: The Osu Collections Editor
===============================

![Image of OCE](http://oce.kurocon.nl/images/oce.png)

OCE is a small program to easily edit osu! collections. The program can edit the collection.db file from the game directly, using your own osu! song database. The program can find any songs that are missing from your song database, but are present in your collections! These songs do not show up in game, but are still in your collections. OCE can see these songs, and try to identify them using the osu! API. This way you can find that one song that you know was in your collection somewhere, but you lost in the game.
  
Table of contents
=================
  * [OCE: The Osu Collections Editor](#oce-the-osu-collections-editor)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Opening your collections](#opening-your-collections)
    * [Adding/Removing/Renaming collections](#addingremovingrenaming-collections)
    * [Adding/Removing songs to a collection](#addingremoving-songs-to-a-collection)
    * [The Add Songs Dialog](#the-add-songs-dialog)
    * [Saving your changes](#saving-your-changes)
    * [Finding missing songs](#finding-missing-songs)
  * [Common problems](#common-problems)
  * [Contributing](#contributing)
    * [Reporting bugs](#reporting-bugs)
    * [Contributing code](#contributing-code)
    * [Contributing art/translations/etc.](#contributing-arttranslationsetc)

Installation
============
There are two ways of installing OCE. Using the precompiled release binaries, or running the application from source.

Release binaries
----------------
You can download the releases from the GitHub releases page <add link here>. Two types of releases are available, standard and portable. 

The standard release is the recommended one. It contains all dependencies of OCE and is meant to run from a folder on your computer. 

The portable release is a little bit slower then the normal release, but has the added benefit of having all dependencies and the application packed into one executable with a few support files. This release is meant to be put on something like a USB stick or something. This way, it is possible to have both the Linux and Windows versions of the program in one place.

The installation for both releases is the same, aside from the archive you download. The installation procedure is as follows

  1. Download the archive for your OS and desired version. (e.g. "OCE_Windows_v1.0.zip" for the  standard release on Windows or "OCE_Linux_Portable_v1.0.tar.gz" for the portable release on Linux)
  3. Extract the downloaded archive somewhere. It does not really matter where.
  2. In the extracted folder, run `oce.exe` on Windows or `oce` on Linux.

The application should now start up normally. If it does not, see [Common problems](#common-problems) below.

Usage
=====

Opening your collections
------------------------
When you start up the program, the first thing you want to do is open up your collections database so you can get to editing! To do that, click `File`, followed by `Open`. (Or press `Ctrl+O`)

![Open collection dialog](http://oce.kurocon.nl/images/open.png)

A popup opens asking you for the location of your osu! songs directory and your collection.db file. There are normally both found in your osu! installation folder (Typically `C\Program Files\osu!` or `C:\Users\(your_username)\AppData\Local\osu!`) but you can also open collection databases downloaded from others or archived song directories.

You can set defaults for both of these values in the [Settings](#settings) so you don't have to fill them in each time!

After giving OCE the location of your songs folder and collection.db, click `OK` and OCE will begin to load your songs and collections!

![API download message](http://oce.kurocon.nl/images/api.png)

When OCE is finished loading your songs and collections, it might have found some maps in your collections database which you do not have in your songs folder. If you have an osu! API key set in the [Settings](#settings), it will ask you if you want to look the information for these songs up via the osu! API. This way, you can find out what these songs are and re-download them via either the osu! song page or look for them on bloodcat if they are no longer available.

Please note that OCE might not be able to find information for all of your missing maps, especially if they have been removed from the osu! website. You can hide these popups or disable API lookup in the [Settings](#settings).

Maps which info was downloaded from the osu! API will be marked with a blue icon. Maps which are completely unknown are marked with a yellow icon.

![API and missing icons](http://oce.kurocon.nl/images/main_api_missing.png)

When everything is done, the main screen will show two columns. The left column will contain all your collections (if you have any), and the right will show you the songs in the currently selected collection, if you have one selected. The buttons at the bottom let you add, remove or rename collections and add or remove songs or mapsets.

Adding/Removing/Renaming collections
------------------------------------
![Collection management](http://oce.kurocon.nl/images/collection_buttons.png)
To add, remove or rename collections, use the buttons underneath the left part of the screen.
The add button lets you create new collections. 
The remove button removes the currently selected collection. 
The edit button lets you rename the selected collection. 
The up and down buttons let you move collections up or down. This will affect how they show up in the osu! client, even if they are not sorted alphabetically. Osu! willreset the order of the collections if you add, remove or rename a collection in the osu! client itself, so if you want to keep your ordering, edit them using this program, and not the osu! client.
The options menu contains all of the above actions. This menu can also be found when right-clicking a collection.

Adding/Removing songs to a collection
-------------------------------------
![Song management](http://oce.kurocon.nl/images/song_buttons.png)
When you have a collection selected in the left part of the screen, the songs in that collection will show up on the right part. To add or remove songs or mapsets, use the buttons below the list.
The add button will open a popup in which you can choose which songs to add. More information on the Add Songs dialog is [below](#the-add-songs-dialog).
The remove button will remove all selected songs from the collection. If a mapset is selected along with normal songs, all songs inside will be removed.
The remove set button will remove all songs in the selected mapsets. If a normal song is selected, all songs in its mapset will also be removed!
The options menu contains all of the above actions, plus two more. This menu can also be found when right-clicking a song or mapset.
The `Open download page` option in the menu will open the download page of the song on the osu! website, if OCE knows about it.
The `Search map on bloodcat` option in the menu will open the bloodcat search page, with the beatmap ID filled in. This allows you to try and find the beatmap on bloodcat if the beatmap is removed from the osu! website or if you cannot download from the normal site for some reason.

The Add Songs Dialog
--------------------
![Add Songs dialog](http://oce.kurocon.nl/images/add_songs.png)
When you click the `Add song` button in the main window, OCE will load all of the songs in your song directory into a list, in which you can pick and choose the songs or mapsets you want to add to the currently selected collection. You can search in the list by typing into the search box below the list.
By using the buttons in the center to add songs to the left list, you pick which songs are going to be added. The double-arrow buttons add or remove the entire mapset of the song selected, and the single arrows only add the selected songs, not the entire mapset.
When you're done picking songs, click `OK` and the maps will be added to the collection. Don't forget to save!

Saving your changes
-------------------
To save all of the changes you made to your collections, click `File` followed by either `Save` or `Save as...`. `Save` will directly save and overwrite the openend collection.db file, and `Save as...` lets you pick where you want to save the database and how to name it.

Finding missing songs
---------------------
One of the features of OCE is to show you a list of maps which you have in one of your collections, but do not have in your songs folder. You can show this list by pressing the `Tools` menu, followed by `Missing beatmaps`. This dialog looks different depending on what kinds of missing songs you have.
![Missing unidentified beatmaps](http://oce.kurocon.nl/images/missing_unidentified_maps.png)
If you only have unidentified missing maps (maps OCE knows nothing about), then it will show a list of the md5 hashes of those maps.
![Missing identified beatmaps](http://oce.kurocon.nl/images/missing_identified_maps.png)
If you only have identified missing maps (maps OCE found via the osu! API) then it will show you the map details, and will give you buttons to open the osu! beatmap page for the map or search for the map on bloodcat.
![Missing both types of beatmaps](http://oce.kurocon.nl/images/missing_maps.png)
If you have both types of missing songs, the dialog will show both lists.
![No missing beatmaps](http://oce.kurocon.nl/images/no_missing_maps.png)
If you have no missing maps, the dialog will show that, too.
You can try to look up beatmaps using the osu! API when you load your collection, or do it manually via the `Tools`->`Match with osu! API` menu option.

Common problems
===============
**OCE is not starting.**
The primary cause of OCE not starting is missing libraries or resource files. The best fix is to redownload and re-extract the application. Make sure that everything that is in the archive is in the same directory as `oce.exe` or `oce`. If that does not fix your issue, check the `oce.log` file in the application directory, that might give some clues. If the log file is empty, you can try to follow the basic [bug reporting](#reporting-bugs) guide to change your log level to debug mode. This shows more information in the log file. If you still cannot start the application, please let me know via a [bug report](#reporting-bugs). 

Contributing
============
I appreciate any contribution you want to make to OCE. You are awesome. I only ask that you try to follow the steps below if you want to help. 

Reporting bugs
--------------
This software probably contains a bunch of bugs which I did not notice during programming. If the program crashes on you for some reason, or does not work as you expect it to, you can do the following.
The program generates a logfile, called `oce.log` in the application directory. Whenever something strange happens, this is probably the file that's going to tell me what went wrong. By default though, the file does not contain much. If you can reproduce the strange behaviour by doing what you did to make it happen again, then set the log level of the application to debug as described below, then make the bug happen. Afterwards send me an email at `oce_bugs@kurocon.nl` with exactly how to make the bug happen, what you think should happen, and the log file as an attachment. If you cannot reproduce the bug, sending me the first log file might be able to help me as well. I'll try to respond to all bug reports, but it might take me a while.

***Lowering the log level to 'DEBUG'***
In the application directory, edit the file `logging.conf` with your favourite editor, like notepad. In the file, there are three lines which say either `level=INFO` or `level=DEBUG`. Change all those to say `level=DEBUG` and save the file to lower the log level.

Requesting new features, sharing ideas, etc.
--------------------------------------------
If you think you have a good idea for the application, I'm ready to hear it. Drop me an email on `oce_ideas@kurocon.nl` telling me about your idea in as much detail as you can. I will try to respond to all ideas, but it might take a while.

Contributing code
-----------------
If you want to implement a new feature for yourself, or fix a bug in the code, you are free to do so. You can fork the repository to your own GitHub account and edit whatever you like, then submit a pull request so I can take a look at what you've built. If I think it looks good, I'll merge it into the code and add you as a contributor to the application's about page. For more instructions on how to setup your development environment, see the developing readme, `development_guide.md`.

Contributing art/translations/etc.
----------------------------------
Any art, translations, whatever, you want to share for the application are gladly accepted, you can drop me an email at `oce@kurocon.nl` with all your contributions or questions, and I'll try to respond to as much as I can.
