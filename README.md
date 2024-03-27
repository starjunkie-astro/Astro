# Discord Bot for N.I.N.A. AutoFocus

The Discord Bot script runs continuously from a server, whether it's Linux or otherwise. It actively communicates with the Discord channel of your choice, ensuring that the Discord bot remains active to monitor uploads of N.I.N.A. AutoFocus JSON files.

## AutoFocus Watchdog Script

The AutoFocus Watchdog script utilizes the Python watchdog module to monitor the N.I.N.A. AutoFocus folder for any new JSON files added to the directory. Upon detecting a new file, it automatically uploads it to the Discord server that you specify.

## Execution within N.I.N.A. Plugin

Using `pyinstaller`, an executable has been created that can be run within a N.I.N.A. plugin known as Sequencer Powerups. You can employ the 'External Script' function in your Advanced Sequencer to initiate the watchdog process seamlessly.
