# Arrowverse-Reorderer

The aim of this project is ordering all the Arrowverse tv series episodes to watch them chronologically.

This package scans for media in provided folders using [mnamer](https://pypi.org/project/mnamer/), then it prepends to all Arrowverse episodes its order number based on [Arrowverse Episode Order](https://arrowverse.info/) website and moves all the episodes to a new folder.

## Install
```
pip install arrowverse-reorderer
```

## Usage
```
usage: arrowverse-reorderer [-h] [-sm] [-dm] [-dr] [-dest [DESTINATION_PATH]] [FOLDERS ...]

Order Arrowverse episodes files in air time order.

positional arguments:
  [FOLDERS]: folders to process

options:
  -h, --help: show this help message and exit
  -sm, --skip-rename: skips rename of files
  -dm, --dry-run-rename: does not really rename files, just prints them (and then exits, equivalent to "mnamer --test")
  -dr, --dry-run-reorder: does not really reorder files, just prints them
  -dest [DESTINATION_PATH], --destination-path [DESTINATION_PATH]: destination folder
```

## Example
Before:
```
+---Supergirl S1
|       Supergirl - S01E01 - Pilot.mp4
|       Supergirl - S01E11 - Strange Visitor from Another Planet.mp4
|       Supergirl - S01E18 - Worlds Finest.mp4
|       Supergirl - S01E20 - Better Angels.mp4
|       
+---The Flash S2
|       The Flash - S02E20 - Rupture.mp4
|       The Flash - S02E21 - The Runaway Dinosaur.mp4
|       The Flash - S02E22 - Invincible.mp4
|       The Flash - S02E23 - The Race of His Life.mp4
|       
\---Vixen S2
        Vixen - S02E01 - Episode 1.avi
        Vixen - S02E02 - Episode 2.avi
        Vixen - S02E03 - Episode 3.avi
        Vixen - S02E04 - Episode 4.avi
        Vixen - S02E05 - Episode 5.avi
        Vixen - S02E06 - Episode 6.avi
```
After:
```
+---reordered
|       118 - Supergirl - S01E01 - Pilot.mp4
|       143 - Supergirl - S01E11 - Strange Visitor from Another Planet.mp4
|       169 - Supergirl - S01E18 - Worlds Finest.mp4
|       177 - Supergirl - S01E20 - Better Angels.mp4
|       183 - The Flash - S02E20 - Rupture.mp4
|       186 - The Flash - S02E21 - The Runaway Dinosaur.mp4
|       189 - The Flash - S02E22 - Invincible.mp4
|       192 - The Flash - S02E23 - The Race of His Life.mp4
|       200 - Vixen - S02E01 - Episode 1.avi
|       205 - Vixen - S02E02 - Episode 2.avi
|       210 - Vixen - S02E03 - Episode 3.avi
|       215 - Vixen - S02E04 - Episode 4.avi
|       219 - Vixen - S02E05 - Episode 5.avi
|       224 - Vixen - S02E06 - Episode 6.avi
|       
+---Supergirl S1
+---The Flash S2
\---Vixen S2
```