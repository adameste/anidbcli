anidbcli
===========================
Anidbcli is a simple command line interface for managing your anime collection on your local computer or NAS (using only ssh).

Requirements
---------------------------
    * `Python 3.6 <https://www.python.org/downloads/>`_ or newer (version 3.5 seems to work as well)

Key features
---------------------------
    * ed2k hashing library utilizing multiple cores
    * adding anime to mylist
    * utilize data from anidb to move/rename the files
    * moves/renames the subtitle and other files with same extension
    * encryption

Installation
---------------------------

The package can be installed automatically using pip.

.. code-block:: bash

   pip install anidbcli
   pip install --upgrade anidbcli #update

Package can be also installed from source like this.

.. code-block:: bash

    python setup.py install

After installation anidbcli can be invoked like a python module

.. code-block:: bash

    python -m anidbcli

or directly by typing following in the command line

.. code-block:: bash

    anidbcli

Quickstart
---------------------------
The basic syntax is

.. code-block:: bash

    anidbcli [OPTIONS] ed2k/api [OPTIONS] ARGS

If you want to just generate ed2k links for mkv and mp4 files recursively for given folders and copy them to clipboard, use:

.. code-block:: bash

    anidbcli -r -e mkv,mp4 ed2k -c "path/to/directory" "path/to/directory2"

Where
    * **-r** is recursive
    * **-e** comma separated list of extensions, that are treated as anime files


To add all mkv files from directory resursively to mylist use:

.. code-block:: bash

    anidbcli -r -e mkv api -u "username" -p "password" -k "apikey" -a "path/to/directory"

Where
    * **"password"** is your anidb password
    * **"username"** is your anidb username
    * **"apikey"** is anidb upd api key, that you can set at http://anidb.net/perl-bin/animedb.pl?show=profile. If no key is provided, unencrypted connection will be used.

Optionally, if you don't provide password or username, you will be prompted to input them.

.. code-block:: bash

    anidbcli -r -e mkv api -k "apikey" -a "path/to/directory"
    Enter your username: "username"
    Enter your password: "password"

To set located files to a specified state use:

.. code-block:: bash
        
        anidbcli -r -e mkv api -u "username" -p "password" -k "apikey" --state 0 -a "path/to/directory"

The number 0 can be substituted for different states:
        * 0 is unknown (default)
        * 1 is internal storage
        * 2 is external storage
        * 3 is deleted
        * 4 is remote storage

To rename all mkv and mp4 files in directory recursively using data from api you can call

.. code-block:: bash

    anidbcli -r -e mkv,mp4 api -u "username" -p "password" -k "apikey" -sr "%ep_no% - %ep_english% [%g_name%]" "path/to/directory"

Where
    * **"-r"** rename using provided format string
    * **"-s"** prepend original file path to each renamed file. Without this flag the files would me moved to current directory.

Also along with the parameter "-r" you can use one of the following parameters:
    * **"-h"** Create hardlinks instead of renaming.
    * **"-l"** Create softlinks instead of renaming.
    * **"-t"** Save session info instead of logging out (session lifetime is 35 minutes after last command). Use for subsequent calls of anidbcli to avoid api bans.

    Anidbcli should be called with all the parameters as usual. If the session was saved before more than 35 minutes, a new session is created instead.
	
You can also move watched anime from unwatched directory to watched directory and add it to mylist at the same time using following command.

.. code-block:: bash

    anidbcli -r -e mkv,mp4 api -u "username" -p "password" -k "apikey" -xr "watched/%a_english%/%ep_no% - %ep_english% [%g_name%]" "unwatched/anime1" "unwatched/anime2"

Where
    * **"-x"** Delete empty folders after moving all files away.

**NOTE: All files with same name and different extension (fx. subtitle files) will be renamed/moved as well.**

Selected usable tags:
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
	
Complete list of usable tags in format string:

.. code-block::  bash

    %fid%, %aid%, %eid%, %gid%, %lid%, %status%, %size%, %ed2k%, %md5%, %sha1%, %crc32%, %color_depth%,
    %quality%, %source%, %audio_codec%, %audio_bitrate%, %video_codec%, %video_bitrate%, %resolution%,
    %filetype%, %dub_language%, %sub_language%, %length%, %aired%, %filename%, %ep_total%, %ep_last%, %year%,
    %a_type%, %a_categories%, %a_romaji%, %a_kanji%, %a_english%, %a_other%, %a_short%, %a_synonyms%, %ep_no%,
    %ep_english%, %ep_romaji%, %ep_kanji%, %g_name%, %g_sname%, %version%, %censored%
