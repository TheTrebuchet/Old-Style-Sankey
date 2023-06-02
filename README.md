# Sankey-generator

Generator of sankey diagrams in the old style

## Install

There isn't much you can do really, this software isn't "prepared" in any way for installation, it's just a simple python file

My recommendation is that you should go to a convenient place in your system, like documents and type in this:

`git clone https://github.com/TheTrebuchet/Old-Style-Sankey.git`

and a directory will emerge, if you want to update the repo just do `git pull` anywhere in the directory

Obviously if you put something inside examples it will get overwritten, if you feel like you really want your example to be here, just contribute on github!
Any `.txt` files in the Old-Style-Sankey folder tho should be fine.

## Basics

In order to use this program, download the folder, run the `python graphic.py` in terminal followed by config.txt file name. It should be located in the same folder but it doesn't have to be, just write the whole path.

## Command options

`--h` shows help

`--unit` accepts a unit, like g/h

`--skew` is a percentage of the whole graphic width at which the inputs and outputs are shifted to the side, 0 disables this effect, default is `0.2`

`--tang` is a multiplier for the cut-outs in input and output blocks, it specified global angle at which they are created, default is `0.4`

`--grid` is an on/off flag that creates the grid

`--unitvalue` accepts a value by which the grid will form, default is 100

## Generating config

Generating the config files is very straight-forward.

### Initiate a row

Place a `#` and specify height with `L` being large and `s` being small. Just like this:

```txt
#s
```

### Initiate blocks

Specify input/operation/output with +/=/- and type in text that will be displayed in the block. *General convention is that blocks should come in a sequence of outputs, operations and inputs, but that's just you choice*

If you want to make loops, just make +@ for loop input and -@ for loop output. Currently only one loop is supported.

```txt
#s
=1038.34 wet bicarbonate
-88.84 loss of CO$_2$
```

New blocks within the row exist are placed simply below. Any kind of python formatting is acceptable.\
Notably `\n` is for newline and `$_a$` is for subscripts and `$^a$` is for superscripts

End your file with a new line with `#`!

### Multi-level blocks

You can create many additional rows within a row.

1. First initiate a row like usual
2. Place some new blocks
3. In the place where multiple rows would exist, just create an indentation and initiate new rows

!!! be sure to make additional height in the top-level row. Say your top level row consists of one small and two L rows, you initiate it by `#sLs` !!!

```txt
#s
=1038.34
-88.84 loss of CO$_2$
#Ls
-916.78 filtrate
    #L
    =121.56 wet bicarbonate
    #s
    =121.56 drying
```

### All text is draggable

change text position to your liking, be aware that while resizing the window still lets you drag it, if you zoom in or out you will lose that ability
