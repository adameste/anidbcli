Basics
============================
There are 2 parameters common for both api and ed2k commands. Those are:
    * **"--recursive"**, **"-r"**: Look for files in given folders recursively.
    * **"--extensions"**, **"-e"**: Specify extensions, that are valid anime files. Program will ignore other files. Accepts a list of extensions (without .) seperated by comma (,). For example "mkv,avi,mp4".

For example to recursively parse all mkv and mp4 files in given folders the arguments would be:

.. code-block:: bash

    anidbcli -r -e mkv,mp4 [ed2k, api] <parameters> FILES