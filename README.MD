##CardRenamer
CardRenamer is a small script that outputs all the player cards in VALORANT with their in-game display name.

###Package requirements
No additional packages are required to run CardRenamer

###Basic instructions
1. Download a VALORANT-compatible version of UModel, such as [this one](https://www.gildor.org/smf/index.php?action=dlattach;topic=7040.0;attach=2029)
2. Get a `locres.json` file, which you can do with [FModel](https://ci.appveyor.com/project/iAmAsval/fmodel/branch/master/artifacts)
3. Run the script once, this will create a file called `paths.json`
4. Fill out the requested paths in `paths.json` such that:  
**valorant_path**: path to your VALORANT installation folder  
**umodel_path**: path to the UModel executable  
**aes_path**: path to the AES key (a text file containing only the key)  
**locres_path**: path to the `locres.json` file  
**extract_path**: working path for the script, **will be DELETED after finishing**  
**target_path**: paths where all the cards will be after finishing
5. Run the script again
6. The cards will now be in `target_path`, enjoy!

###Credits
Gildor for creating UModel [Go](https://www.gildor.org/en/projects/umodel)  
UModel user spiritovod for fixing VALORANT compatibility [Go](https://www.gildor.org/smf/index.php/topic,7040.msg39129.html#msg39129)  
The FModel team for creating it [Go](https://github.com/iAmAsval/FModel)
