import matplotlib.pyplot as plt
from numpy import sign
import sys
 
file = str(sys.argv[1])
if file == None:
    print('you need to specify config.txt file')
    quit()

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
    ax.annotate(name + '\n'+str(round(mass,2)) + 'g/h', xy, ha='center', va='center').draggable()

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
    print(lines)
    rows = []
    mode = 0
    for l in lines:
        if '    #' in l:
            mode+=1
        if mode and '    ' not in l:
            print('indent',mode)
            rows[-(mode+1)].append(rows[-mode:])
            rows = rows[:-(mode)]
            mode = 0
        if '#'in l:
            rows.append([l.strip()[1:]])
        else:
            rows[-1].append(l.strip().split(' ',1))
    rows = [r for r in rows if r!=['']]

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
            print(row)
            print(h)
            for block in row[1:]:
                if not isinstance(block[0],str):
                    rowbyrow(block,[coords[0]+mass,coords[1]])
                    continue
                print(float(block[0][1:]))
                delta(mode[block[0][0]], float(block[0][1:]), h, block[1], [coords[0]+mass,coords[1]], tang,s)
                mass+=float(block[0][1:])
                if block[0][0]=='-':out+=float(block[0][1:])
            coords[1]-=h
            coords[0]+=out
    rowbyrow(rows,coords)
    plt.show()

draw(file)