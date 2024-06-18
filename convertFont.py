import json

# Converts JSON files from https://www.pentacom.jp/pentacom/bitfontmaker2/
# Into C files

# unfortunately, bitfontmaker removes the space character. You need to manually add it to the font.json file:
# For example: "32":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

starty = 7
endy   = 12
startx = 2
endx   = 6

startChar = ' '
endChar = chr(255) # set this to '~' to save program memory

fontname = "tiny5p"


def getMSB(n):
    if (n == 0):
        return 0;
 
    msb = 0;
    n = int(n / 2);
 
    while (n > 0):
        n = int(n / 2);
        msb += 1;
 
    return msb;

def getCharWidth(char):
    maxWidth = 0
    for n in char:
        n >>= startx
        w = getMSB(n)
        maxWidth = max(w, maxWidth)
    return maxWidth + 1;

bitmapname = "font_" + fontname + "_Bitmaps"
descriptorname = "font_" + fontname + "_Descriptors"

outputCdata = "const uint8_t " + bitmapname + "[] = {\n"
outputCdescr = "const FONT_VW_CHAR_INFO " + descriptorname + "[] = {\n"

with open('font.json') as f:
    d = json.load(f)
    
    offset = 0
    for charStr in d:

        if int(charStr) < ord(startChar):
            continue;
        if int(charStr) > ord(endChar):
            break;
        
        l = d[charStr]
        
        if isinstance(l, list):    #make sure we are still getting the character data
            #print(l)
            w = getCharWidth(l)
            #print("width: " + str(w))
            outArr = [0] * w;      #list of zeros
            
            curNum = 0;
            curIndex = 0;

            #convert data to collumn-format
            for num in l:
                if curNum >= starty and curNum <= endy:
                    #ok we are now in the data-zone
                    num >>= startx
                    #if n bit is set, we put it in the outArr at the correct pos according to y
                    #print(num)
                    for i in range(0,w):
                        if num & (1<<i):
                            outArr[i] |= (1<<curIndex)
                            #print("bit found" + str(i))
                    curIndex = curIndex + 1
                curNum = curNum + 1
            
            
            
            name = ""
            #print(charStr)
            print(l)
            #if int(charStr) < 255:
            name = chr(int(charStr))  #name of the character (ASCII representation)
            outputCdata = outputCdata + "// num: " + charStr + ", char: " + name + ",  " + str(w) + " pixels wide\n"

            # draw the character
            for y in range(starty, endy+1):
                outputCdata = outputCdata + "\t//" 
                for x in range(0, w):
                    if (l[y] >> startx) & (1<<x):
                        outputCdata = outputCdata + '#'
                    else:
                       outputCdata = outputCdata + ' ' 
                outputCdata = outputCdata + '\n' 

            
            for num in outArr:
                outputCdata = outputCdata + hex(num) + ","
            outputCdata = outputCdata + "\n"
            
            
            outputCdescr = outputCdescr + "\t{" + str(w) + ", " + str(offset) + "},\n"
            offset = offset + w
            
            #print(char + str(outArr) + "width: " + str(w))

    outputCdata = outputCdata + "};\n\n"
    outputCdescr = outputCdescr + "};\n\n"
    
    outputCInfo = "const FONT_INFO font_" + fontname + "_FontInfo = \n{\n\t"
    outputCInfo = outputCInfo + "1, /*character height*/\n\t '" + startChar + "', /*  Start character */\n\t"
    outputCInfo = outputCInfo + "'" + endChar + "',  /*  End character */\n\t"
    outputCInfo = outputCInfo + descriptorname + ",\n\t" + bitmapname + ",\n\t 0 \n };\n"
        
with open("font_" + fontname + ".c",'w') as outfile:
    outfile.write("#include \"font_" + fontname + ".h\"\n\n")
    outfile.write(outputCdata + outputCdescr + outputCInfo)
    outfile.close()   

with open("font_" + fontname + ".h", 'w') as outfile:
   
    outfile.write("#include \"fonts.h\" \n\n")
    outfile.write("extern const uint8_t " + bitmapname + "[];\n")
    outfile.write("extern const FONT_VW_CHAR_INFO " + descriptorname + "[];\n")
    outfile.write("extern const FONT_INFO font_" + fontname + "_FontInfo;\n")
    outfile.close()  
        