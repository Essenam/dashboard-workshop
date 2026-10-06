# Local data cache

Raw data files go here: the big, row-level files the data quality tests run against.

- **Fill it from the flash drive or the workshop's shared folder.** Copy the monthly trip
  files in as they are. Nothing needs to be downloaded in the room.
- **Git ignores everything in this folder except this note.** Raw data never goes to GitHub:
  the files are too large, and in your own work they may hold things that should not leave
  your laptop.
- **The dashboard never reads these files directly.** The tests read them and write small
  summary files; every chart reads the summaries.

Changed a test? Run it again against the files here. They stay put, so nothing is downloaded
twice.
