# hk-horn
Hollow Knight Mods (Packages) Manager =)

(In current time in Alpha..)

## Installation..
```bash
pip install --upgrade hk_horn
```

## Usage
### Help
```bash
# with `python -m`
python -m horn -h
# or if included in PATH:
horn -h
```
#### output:
```bash
Usage: horn.py [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  find
  info
  install
```

### Mods search
```bash
horn find --display=no --name Hk
```
#### output:
```bash
'HKHKHKHKHK' 1.5.0.0
'HKMP HealthDisplay' 0.0.6.0
'HKMirror' 2.1.0.0
'HKMP' 2.4.1.0
'HKMP Prop Hunt' 0.0.2.1
'HKVR' 0.0.0.0
'HkmpPouch' 1.0.0.0
'SmashKnight' 1.0.0.0
'HKmote' 1.4.0.0
'HKTracker' 3.4.1.1
'HKTool Legacy' 1.11.8.0
'HKTool' 2.2.1.0
'HKTimer' 0.1.1.0
'HKMP.ModDiff' 1.0.2.0
'HKMP Tag' 2.3.1.0
'HKRoomLogger' 1.0.8467.33528
```
or with description
```bash
horn find --name Hk
# or other flag (default description)
horn find --display=link --name Hk
```
#### output:
```bash
'HKHKHKHKHK' 1.5.0.0 - VVVVVVV but in HK. Flip gravity with the R key.
'HKMP HealthDisplay' 0.0.6.0 - An addon for HKMP that uses HkmpPouch. Works on the public server.Displays the amount of health other players have
'HKMirror' 2.1.0.0 - A core mod that makes it easier to access PlayerData, use reflection, and on/il hooks.
'HKMP' 2.4.1.0 - Hollow Knight Multiplayer allows people to host games and let others join them in their adventures.
'HKMP Prop Hunt' 0.0.2.1 - An HKMP add-on that adds Prop Hunt to multiplayer games.
'HKVR' 0.0.0.0 - Play Hollow Knight in virtual reality.
'HkmpPouch' 1.0.0.0 - A dependency mod for optional hkmp addons with networking.
'SmashKnight' 1.0.0.0 - Changes Knight handling based on health remaining.
'HKmote' 1.4.0.0 - Use emotes during multiplayer
'HKTracker' 3.4.1.1 - Tracks player data. Most frequently used to display abilities/charms during streams
'HKTool Legacy' 1.11.8.0 - A library mod.No longer maintained!!!**If it crashes your game, this is normal and the reason is unknown**
'HKTool' 2.2.1.0 - A library mod
'HKTimer' 0.1.1.0 - An in game timer mod for 1.5
'HKMP.ModDiff' 1.0.2.0 - HKMP Addon for checking mod lists between Clients and Servers.
'HKMP Tag' 2.3.1.0 - An HKMP addon that adds the tag game-mode.
'HKRoomLogger' 1.0.8467.33528 - Logs scene transitions to a file. Companion mod to Windows-only software HKAT.
```

### Mod info
```bash
horn info HKMP
```
or
```bash
horn info HKMP --version 2.4.1.0
```
#### output:
```bash
Mod(
    name='HKMP',
    description='Hollow Knight Multiplayer allows people to host games and let others join them in their adventures.',
    version='2.4.1.0',
    link='https://github.com/Extremelyd1/HKMP/releases/download/v2.4.1/HKMP.zip',
    dependencies=None,
    repository='https://github.com/Extremelyd1/HKMP/',
    issues=None,
    tags=None,
    authors=['Extremelyd1']
)
```

### Mods installation (will update in future)
```bash
horn install --path="/path/to/game/mods/dir/Games/Hollow Knight/Hollow Knight_Data/Managed/Mods" 'HKMP','Satchel'
```
#### output:
```bash
[11/19/23 23:01:24] INFO     Searching package 'HKMP'                                                                                                                                                     api.py:402
                    INFO     Searching field(s) ptrn(s) `{'name': '^HKMP$'}`                                                                                                                              api.py:289
                    INFO     Installing package `'HKMP'==2.4.1.0`                                                                                                                                         api.py:423
[11/19/23 23:01:27] INFO     File exists in cache `~/.cache/horn/pkg/HKMP.zip`                                                                                                                  api.py:362
                    INFO     Unpacking `~/.cache/horn/pkg/HKMP.zip` to path `~/PortWINE/PortProton/prefixes/DEFAULT/drive_c/Games/Hollow Knight/Hollow Knight_Data/Managed/Mods/HKMP` api.py:386
                    INFO     Installation of package `'HKMP'==2.4.1.0` complete!                                                                                                                          api.py:432
Status:  OK
                    INFO     Searching package 'Satchel'                                                                                                                                                  api.py:402
                    INFO     Searching field(s) ptrn(s) `{'name': '^Satchel$'}`                                                                                                                           api.py:289
                    INFO     Installing package `'Satchel'==0.8.12.0`                                                                                                                                     api.py:423
[11/19/23 23:01:28] INFO     Downloading `https://github.com/PrashantMohta/Satchel/releases/download/v0.8.12/Satchel.zip` to path `~/.cache/horn/pkg/Satchel.zip`                               api.py:365
[11/19/23 23:01:30] INFO     Unpacking `~/.cache/horn/pkg/Satchel.zip` to path `~/PortWINE/PortProton/prefixes/DEFAULT/drive_c/Games/Hollow Knight/Hollow                             api.py:386
                             Knight_Data/Managed/Mods/Satchel`                                                                                                                                                      
                    INFO     Installation of package `'Satchel'==0.8.12.0` complete!                                                                                                                      api.py:432
Status:  OK
```
