import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from matplotlib import rc
from numpy import sign
import argparse
import re

#for preparing the info about a single block
class block:
    def __init__(self, line):
        first = line.split()[0]
        self.delta = re.sub(r'[0-9\.]', '', first)
        self.value = float(re.sub('[^0-9\.]', '', first))
        self.name = line.split(' ',1)[1].replace('\\n','\n')

#for drawing the box
def delta(typ, mass, height, name, coords, tang, skew):
    insert = tang*mass/2
    if insert>0.2*height:insert=0.2*height
    
    geo = {
    '=' : [[0,0], [mass, 0], [mass, -height], [0, -height], [0,0]],
    '+' : [[0,0], [mass/2, -insert], [mass, 0], [mass, -height], [0, -height], [0,0]], 
    '-' : [[0,0], [mass, 0], [mass, -height], [mass/2, -height-insert], [0, -height], [0,0]],
    '+@' : [[mass, 0], [mass, -height], [0, -height], [0,0]],
    '-@' : [[0, -height], [0,0], [mass, 0], [mass, -height]]
    }
    verts = geo[typ]
    if typ=='-': verts = [[i[0]+i[1]*skew, i[1]] for i in verts]
    if typ=='+': verts = [[i[0]+(i[1]+height)*skew, i[1]] for i in verts]
    verts = [[i[0]+coords[0],i[1]+coords[1]] for i in verts]
    
    #xy is coordinates of name
    xy = [mass/2, -height/2]
    if typ=='+': xy[0] += -xy[1]*skew +coords[0]
    else: xy[0] += xy[1]*skew +coords[0]
    xy[1] += coords[1]
    for i in range(len(verts)-1):
        plt.plot((verts[i][0],verts[i+1][0]), (verts[i][1],verts[i+1][1]), c='black',zorder=1)
    ax.annotate(name + '\n'+str(round(mass,2)) + args.unit, xy, ha='center', va='center',zorder=2).draggable()

#draws the whole figure, THE IMPORTANT PART
def rowbyrow(rows,coords):
    for row in rows:
        h = sum(height[i] for i in row[0])
        mass = 0
        out = 0
        ind = rows.index(row)
        if ind == 0 or ind == len(rows)-1:s = 0
        else:s=skew
        for entry in row[1:]:
            if not isinstance(entry,block):
                rowbyrow(entry,[coords[0]+mass,coords[1]])
                #if last blocks were outputting, the coords are updated accordingly
                coords[0] += sum([b.value for b in entry[-1][1:] if '-' in b.delta])
                continue
            if '@' in entry.delta: 
                loop.append([entry,coords.copy(), h])
            delta(entry.delta, entry.value, h, str(entry.name), [coords[0]+mass,coords[1]], tang, s)
            mass+=float(entry.value)
            if '-' in entry.delta: out+=float(entry.value)
        coords[1]-=h
        coords[0]+=out

def loopygoop(loop, glw, glh, ax):
    r = 10
    margin = 2
    ratio = glh/glw
    stent, stco, sth, enent, enco, enh = [a for b in loop for a in b]
    plt.plot((stco[0]-r,-r-margin),(stco[1]+r*ratio,stco[1]+r*ratio),c='black',zorder=1)
    plt.plot((stco[0]-r,-r-margin),(stco[1]+(r+stent.value)*ratio,stco[1]+(r+stent.value)*ratio),c='black',zorder=1)
    plt.plot((enco[0]-r,-r-margin),(enco[1]-enh-r*ratio,enco[1]-enh-r*ratio),c='black',zorder=1)
    plt.plot((enco[0]-r,-r-margin),(enco[1]-enh-(r+enent.value)*ratio,enco[1]-enh-(r+enent.value)*ratio),c='black',zorder=1)
    plt.plot((-2*r-margin, -2*r-margin),(stco[1], enco[1]-enh),c='black',zorder=1)
    plt.plot((-2*r-margin-stent.value, -2*r-margin-enent.value),(stco[1],enco[1]-enh),c='black',zorder=1)
    ax.add_patch(ptc.Arc((-r,stco[1]), 2*r, 2*r*ratio, angle=0.0, theta1=0, theta2=90, linewidth=1))
    ax.add_patch(ptc.Arc((-r,stco[1]), 2*(r+stent.value), 2*(r+stent.value)*ratio, angle=0.0, theta1=0, theta2=90, linewidth=1))

    ax.add_patch(ptc.Arc((-r-margin,stco[1]), 2*r, 2*r*ratio, angle=0.0, theta1=90, theta2=180, linewidth=1))
    ax.add_patch(ptc.Arc((-r-margin,stco[1]), 2*(r+stent.value), 2*(r+stent.value)*ratio, angle=0.0, theta1=90, theta2=180, linewidth=1))

    ax.add_patch(ptc.Arc((-r-margin,enco[1]-enh), 2*r, 2*r*ratio, angle=0.0, theta1=180, theta2=270, linewidth=1))
    ax.add_patch(ptc.Arc((-r-margin,enco[1]-enh), 2*(r+enent.value), 2*(r+enent.value)*ratio, angle=0.0, theta1=180, theta2=270, linewidth=1))

    ax.add_patch(ptc.Arc((-r,enco[1]-enh), 2*r, 2*r*ratio, angle=0.0, theta1=270, theta2=360, linewidth=1))
    ax.add_patch(ptc.Arc((-r,enco[1]-enh), 2*(r+enent.value), 2*(r+enent.value)*ratio, angle=0.0, theta1=270, theta2=360, linewidth=1))
    
    offsetx = max(stco[0]+stent.value+margin+2*r, 0)
    offsety = max(stco[1]+(r+stent.value)*ratio, 0)
    glw += offsetx
    glh = offsety + max(-enco[1]+enh+(r+enent.value)*ratio, glh)
    return offsetx, offsety, glw, glh

#FONTS
font = {'family':'serif'}
rc('font', **font)
 

#ARGUMENTS
parser = argparse.ArgumentParser(
                    prog='ClassicSankeyGen',
                    description='Creates Sankey diagrams',
                    epilog='Just read readme if you feel lost')

parser.add_argument('filename')
parser.add_argument('-u', '--unit')
parser.add_argument('-uv', '--unitvalue',default = 100)
parser.add_argument('-s', '--skew',default = 0.2)
parser.add_argument('-t', '--tang',default = 0.4)
parser.add_argument('-m', '--margin',default = 0.1)
parser.add_argument('-g', '--grid', action='store_true')  # on/off flag
args = parser.parse_args()

if not args.unit:
    print('you need to specify the unit\nadd for example \"-u g/h\"')
    quit()

#default simple settings, mostly turning off axes and other plot things
w, h = 10, 10
fig = plt.figure(frameon=True)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

#converts config to readable array
with open(args.filename,encoding='utf-8', errors='ignore') as content:
    lines = content.readlines()
lines = [i.rstrip('\n') for i in lines if i != '\n']
rows = []
level = 0
for l in lines:
    if '    #' in l or '\t#' in l:
        level+=1
    if level and '    ' not in l and '\t' not in l:
        rows[-(level+1)].append(rows[-level:])
        rows = rows[:-level]
        level = 0
    if '#'in l:
        rows.append([l.strip()[1:]])
    else:
        rows[-1].append(block(l.strip()))
rows = [r for r in rows if r!=['']]

#dictionaries
L_height = 0.2
s_height = 0.1
height = {'L':L_height,'s':s_height}

#from rows
globalwidth = sum([float(re.sub('[^0-9\.]', '', l.split()[0])) for l in lines if '+' in l])
globalheight = sum([sum([height[el] for el in l[1:]]) for l in lines if '#' in l and '    ' not in l and '\t' not in l])

#settings
skew = globalwidth*args.skew
tang = globalheight/globalwidth*args.tang
coords = [0,0]
loop = []

#drawing the whole thing
rowbyrow(rows,coords)
#drawing the loop
loopmargin = 0
offsetx = 0
offsety = 0
if loop: 
    offsetx, offsety, globalwidth, globalheight = loopygoop(loop, globalwidth, globalheight, ax)

#for creating grid
def grid(width, height, margin, unit, offsetx, offsety):
    plt.axis([-margin*width-offsetx, (1+margin)*width-offsetx, -(1+margin)*height, margin*height+offsety])

    hunit = unit*height/width

    limx = int((1+2*margin)*(width)//unit+1)
    limy = int((1+2*margin)*(height)//hunit+1)
    
    for i in range(limx):
        x = i*unit-margin*width+(margin*width)%unit-offsetx
        plt.plot([x,x],[-(1+margin)*height, margin*height+offsety],zorder=0,c='lightgray',linestyle='--')
    
    for i in range(limy):
        y = -i*hunit+margin*height-(margin*height)%hunit+offsety
        plt.plot([-margin*width-offsetx, (1+margin)*width],[y,y],zorder=0,c='lightgray',linestyle='--')

    start = [-margin*width+unit+(margin*width)%unit-offsetx, margin*height-(margin*height)%hunit-(limy-1)*hunit+offsety]
    end = [start[0]+unit,start[1]]
    
    textco = [start[0]+0.5*unit,start[1]+0.5*hunit]
    ax.annotate("", xy=start, xytext=end, arrowprops={'arrowstyle':'<->', 'shrinkA': 0, 'shrinkB': 0},zorder=2).draggable()
    ax.annotate(str(unit)+str(args.unit), textco, ha='center', va='top',zorder=2).draggable()
    
if args.grid:
    grid(globalwidth, globalheight,float(args.margin),float(args.unitvalue), offsetx,offsety)
plt.show()


