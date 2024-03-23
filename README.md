The Discord bot script runs always from a server, Linux or otherwise.  It constantly speaks to the Discord channel of your choice, and keeps the Discord bot active to watch for uploads of N.I.N.A. AutoFocus JSON files.

The AutoFocus-Discord script uses the Python watchdog module to watch the N.I.N.A. AutoFocus folder for any new JSON files added to the directory.  When that happens it uploads it to the Discord server you specify.
