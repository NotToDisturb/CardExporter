## CardRenamer
CardRenamer is a small script that outputs all the player cards in VALORANT with their in-game display name.
It uses Python 3.8.

### Instructions
1. Download a VALORANT-compatible version of UModel, such as [this one](https://www.gildor.org/smf/index.php?action=dlattach;topic=7040.0;attach=2029)
2. Download [QuickBMS](http://aluigi.altervista.org/papers/quickbms.zip)
3. Download the [UnrealTournament4 script](http://aluigi.org/bms/unreal_tournament_4.bms)
4. Download [locres2csv](https://drive.google.com/open?id=1-ftM3xAukoogkU5SmNKmsXYLA4b6omgJ)
5. Run the script once, this will create two files called `cards_config.json` and `locres_config.json`
6. Fill out the requested paths in `cards_config.json` and `locres_config.json`
7. Run the script again
8. The cards will now be in `target_path`, enjoy!

## Regarding `cards_config.json`
**valorant_path**: path to your VALORANT installation folder.  

**umodel_path**: path to the UModel executable.  

**aes_path**: path to the AES key (a text file containing only the key).  

**locres_path**: path to the `locres.json` file.  
It will be exported to and read from this path.

**extract_path**: working path for the script, **WILL BE DELETED AFTER THE SCRIPT ENDS**.  

**target_path**: path where all the cards will be after the script ends.

### Regarding `locres_config.json`
**quickbms_path**: path to the QuickBMS executable.

**ut4_path**: path to the UnrealTournament4 script.

**l2c_path**: path to the locres2csv executable.

**aes_path**: path to the AES key (a text file containing only the key).

**valorant_path**: path to your VALORANT installation folder.

**working_path**: path where the extraction of `Game.locres` and its parsing to CSV will take place.  
The `Game.locres` file will not be kept after the script ends.

### Credits
Gildor for creating UModel [Go](https://www.gildor.org/en/projects/umodel)  
UModel user spiritovod for fixing VALORANT compatibility [Go](https://www.gildor.org/smf/index.php/topic,7040.msg39129.html#msg39129)  
Luigi Auriemma for creating QuickBMS [Go](https://aluigi.altervista.org/)  
akintos for creating locres2csv [Go](https://zenhax.com/viewtopic.php?t=1022&start=40)
