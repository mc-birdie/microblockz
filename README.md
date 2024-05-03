Uses block data from the [tellMe](https://www.curseforge.com/minecraft/mc-mods/tellme) mod to translate a list of block names into (hopefully) usable configs for forge microblocks. The main use of this script is that it adds ranges `:0-15` to most blocks that have variations.

**This script was written for and used with a pack running `1.12.2` and it may not work for you in other versions! (It also may work for you!! I have no idea, try it out!)**

usage: `python3 main.py dump.txt blocklist.txt out.txt`

After running the command you can paste the contents of `out.txt` into `/config/microblocks.cfg`.

`dump.txt`, `blocklist.txt`, and `out.txt` are **filenames** _not paths_. The script
assumes these files live top-level and that you are executing the script from top-level.

Searches dump.txt for items that match those in blocklist.txt and spits out
(hopefully) valid data into out.txt

The sample `blocklist.txt` file in this repository was generated in `1.12.2` using the [tellMe](https://www.curseforge.com/minecraft/mc-mods/tellme) mod using the `/tellme dump-json blocks` command.

There is custom code to handle `xtones` because that mod does not output its block variants the same way
other mods do. It is possible you could use something like `/tellme dump-json blocks-with-nbt` (or one of the
other commands listed in that mod's documentation) to get these values, but I didn't put that much time into it.

I'm happy to accept PRs to enhance this code if anyone wants to submit them.