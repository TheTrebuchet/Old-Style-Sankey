# Sankey-generator

Generator of sankey diagrams in the old style

If you want quick summary of what you can do run `python graphic.py -h` and look at the example file.

## Command options

`--h` shows help \

`--unit` accepts a unit, like g/h

`--skew` is a percentage of the whole graphic width at which the inputs and outputs are shifted to the side, 0 disables this effect, default is `0.2`

`--tang` is a multiplier for the cut-outs in input and output blocks, it specified global angle at which they are created, default is `0.4`

`--grid` is an on/off flag that creates the grid and currently it's not working

## Generating config

Generating the config files is very straight-forward.

### Initiate a row

Place a `#` and specify height with `L` being large and `s` being small. Just like this:

```txt
#s
```

### Initiate blocks

Specify input/operation/output with +/=/- and type in text that will be displayed in the block.

```txt
#s
=1038.34 wet bicarbonate
-88.84 loss of CO$_2$
```

New blocks within the row exist are placed simply below. Any kind of python formatting is acceptable.\
Notably `\n` is for new line and any `$_a$` is for subscripts and `$^a$` is for superscripts

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
