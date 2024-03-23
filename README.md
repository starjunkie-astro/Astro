The Discord Bot script runs always from a server, Linux or otherwise.  It constantly speaks to the Discord channel of your choice, and keeps the Discord bot active to watch for uploads of N.I.N.A. AutoFocus JSON files.

The AutoFocus Watchdog script uses the Python watchdog module to watch the N.I.N.A. AutoFocus folder for any new JSON files added to the directory.  When that happens it uploads it to the Discord server you specify.

Running pyinstaller, I created an executable you can run within a N.I.N.A. plugin called Sequencer Powerups.  Use the 'External Script' function in you Advanced Sequencer to start the watchdog process.
