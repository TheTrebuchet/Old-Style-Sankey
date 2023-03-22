import matplotlib.pyplot as plt
from numpy import sign
import argparse
 
parser = argparse.ArgumentParser(
                    prog='ClassicSankeyGen',
                    description='Creates Sankey diagrams',
                    epilog='Just read readme if you feel lost')

parser.add_argument('filename')           # positional argument
parser.add_argument('-u', '--unit')      # option that takes a value
parser.add_argument('-g', '--grid', action='store_true')  # on/off flag
args = parser.parse_args()

if not args.unit:
    print('you need to specify the unit\nadd for example \"-u g/h\"')
    quit()

class block:
    def __init__(self, line):
        mode = {'+':1,'=':0,'-':-1}
        self.delta = mode[line[0]]
        self.value = float(line.split(' ',1)[0][1:])
        self.name = line.split(' ',1)[1]



def delta(typ, mass, height, name, coords, tang, skew):
    insert = tang*mass/2
    if insert>0.2*height:insert=0.2*height
    
    geo = [[[0,0], [mass, 0], [mass, -height], [0, -height]],
    [[0,0], [mass/2, -insert], [mass, 0], [mass, -height], [0, -height]], 
    [[0,0], [mass, 0], [mass, -height], [mass/2, -height-insert], [0, -height]]]
    verts = geo[typ]

    if typ==-1: verts = [[i[0]+i[1]*skew, i[1]] for i in verts]
    if typ==1: verts = [[i[0]+(i[1]+height)*skew, i[1]] for i in verts]

    verts = [[i[0]+coords[0],i[1]+coords[1]] for i in verts]
    xy = [mass/2, -height/2]
    xy[0] += -xy[1]*sign(typ)*skew +coords[0]
    xy[1] += coords[1]
    for i in range(len(verts)-1):
        plt.plot((verts[i][0],verts[i+1][0]), (verts[i][1],verts[i+1][1]), c='black')
    plt.plot((verts[0][0],verts[-1][0]), (verts[0][1],verts[-1][1]), c='black')
    ax.annotate(name + '\n'+str(round(mass,2)) + args.unit, xy, ha='center', va='center').draggable()

w, h = 10, 10
fig = plt.figure(frameon=True)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

def draw(file):

    with open(file) as content:
        lines = content.readlines()
    lines = [i.replace('\n','') for i in lines if i != '\n']
    rows = []
    mode = 0
    for l in lines:
        if '    #' in l:
            mode+=1
        if mode and '    ' not in l:
            rows[-(mode+1)].append(rows[-mode:])
            rows = rows[:-(mode)]
            mode = 0
        if '#'in l:
            rows.append([l.strip()[1:]])
        else:
            rows[-1].append(block(l.strip()))
    rows = [r for r in rows if r!=['']]

    #settings
    L_height = 0.2
    s_height = 0.1
    skew = (750)/L_height*0.05
    tang = 1.5*L_height/(750)
    coords = [0,0]
    mode = {'+':1,'=':0,'-':-1}
    height = {'L':L_height,'s':s_height}

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
                    continue
                delta(entry.delta, entry.value, h, entry.name, [coords[0]+mass,coords[1]], tang,s)
                mass+=float(entry.value)
                if entry.delta==-1:out+=float(entry.value)
            coords[1]-=h
            coords[0]+=out
    rowbyrow(rows,coords)
    plt.show()

draw(args.filename)