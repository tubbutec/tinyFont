A tiny font based on https://robey.lag.net/2010/01/23/tiny-monospace-font.html
The font is 5px height with a descender of 1px for some charachters.

In order to both reduce width and increase readability some characters were modfied and the monospace font converted into a variable-width font.
While some characters were reduced in width (i,.! )
Others were exteded to a width of 4 pixels (G,Q,a) or 5 pixels (M,N,m) 

The repository contains a json file with the font data, compatible with BitfontMaker2:
https://www.pentacom.jp/pentacom/bitfontmaker2/

As well as a python script to convert these JSON files to C code. The script has only been tested with this font and will not universally work with all font sizes.

Some improvements or variations are possible: 
- One could easily modify this font to have a height of 5 pixels for all characters: Just move g,j,p,q and y up one pixel.
- Reduce the width of some characters further: [ and ] could be reduced to 2 px
