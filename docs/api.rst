api
===============================
This command uses the anidb API to add files to mylist or/and rename them.

options
-------------------------------
This is the complete list of options, some of them will be described further in following sections.
    * **"--username"**, **"-u"**: Your anidb username. Prompt will be displayed if unset.
    * **"--password"**, **"-p"**: Your anidb password. Prompt will be displayed if unset.
    * **"--apikey"**, **"-k"**: To enable encryption, you need to provide your apikey.
    * **"--add"**, **"-a"**: Add the files to mylist as watched.
    * **"--rename"**, **"-r"**: Renames the files using the provided format string.
    * **"--keep-structure"**, **"-s"**: Prepend the old file path to the provided format string.
    * **"--date-format"**, **"-d"**: Date format in python syntax. Default is "%Y-%m-%d". Should not contain any characters, that cannot be in filename.
    * **"--delete-empty"**, **"-x"**: Delete empty folders after moving the files.

encryption
-------------------------------
Anidb UDP api uses custom encryption based on AES128. To use encryption you must set your api key by visiting **Settings -> Account -> UDP API Key** on anidb website.
http://anidb.net/perl-bin/animedb.pl?show=profile

username and password
-------------------------------
You can either pass those using options. If username and password are not passed via options, the user will be propmted to provide missing credenitals.

So you can call either

.. code-block:: bash

    anidb [OPTIONS] api -p password -u username [OTHER_OPTIONS] FILES

or

.. code-block:: bash

    anidb [OPTIONS] api [OPTIONS] FILES
    Enter your username: username
    Enter your password: ********

add
-------------------------------
If this option is enabled, files are added to mylist as added. For example to add all mkv files from folder "Gintama" to mylist use:

.. code-block:: bash

    anidb -r -e mkv api -a -u username -p password -k apikey "Gintama"

rename
-------------------------------
Option to move/rename files based on specified options. For rename option a format string needs to be provided.

For example if you watched Gintama and Naruto and you want to move them to watched folder and add the files to mylist:

.. code-block:: bash

    anidb -r -e mkv api -a -u username -p password -k apikey -r "watched/%a_english%/%ep_no% - %ep_english% [%g_name%][%resolution%]" "unwatched/Gintama" "unwatched/Naruto"

If you wish to keep them in the original folder and just rename them, use the **"-s"** option, which will prepend original directory to format string when renaming. Like:

.. code-block:: bash

    anidb -r -e mkv api -a -u username -p password -k apikey -sr "%a_english%/%ep_no% - %ep_english% [%g_name%][%resolution%]" "anime/Gintama" "anime/Naruto"

If you want to delete empty folders after moving all files, use the **"-x"** option.

.. code-block:: bash

    anidb -r -e mkv api -a -u username -p password -k apikey -xr "watched/%a_english%/%ep_no% - %ep_english% [%g_name%][%resolution%]" "unwatched/Gintama" "unwatched/Naruto"

**NOTE: All files with same name and different extension will be renamed and moved as well. This is important if you have external subtitle files.**

Complete list of usable tags in format string:
    * **%md5%** - md5 hash of file.
    * **%sha1%** - sha1 hash of file.
    * **%crc32%** - crc32 hash of file.
    * **%resolution%** - file resolution, for example "1920x1080"
    * **%aired%** - Episode aired date. Only option that needs "--date-format" option. You can find list of available tags at https://docs.python.org/3.6/library/time.html#time.strftime.
    * **%year%** - Year, the anime was aired. Can be a timespan, if the anime was aired several years "1990-2005" etc.
    * **%a_romaji%** - Anime title in romaji.
    * **%a_kanji%** - Anime title in kanji.
    * **%a_english%** - English anime title.
    * **%ep_no%** - Episode number. Prepends the necessary zeros, fx. 001, 01
    * **%ep_english%** - English episode name.
    * **%ep_romaji%** - Episode name in romaji.
    * **%ep_kanji%** - Episode name in kanji.
    * **%g_name%** - Group that released the anime. fx. HorribleSubs.
    * **%g_sname%** - Short group name.