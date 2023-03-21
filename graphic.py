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
    ax.annotate(name + '\n'+str(round(mass,2)*2) + 'g/h', xy, ha='center', va='center').draggable()

w, h = 10, 10
fig = plt.figure(frameon=True)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

def execute(file):

    with open(file) as content:
        lines = content.readlines()
    lines = [i.replace('\n','') for i in lines if i != '\n']
    rows = []
    mode = 0
    for l in lines:
        if '#' in l and '##' not in l:
            rows.append([l[-1]])
            mode = 0
        elif '##' in l:
            rows[-1].append([l[-1]])
            mode = 1
        elif mode == 0:rows[-1].append(l.split(' ',1))
        elif mode == 1:rows[-1][-1].append(l.split(' ',1))

    L_height = 0.2
    s_height = 0.06

    skew = (750)/L_height*0.05
    tang = 1.5*L_height/(750)

    coords = [0,0]
    
    mode = {'+':1,'=':0,'-':-1}
    height = {'L':L_height,'s':s_height}
    skew_mode = 0
    for row in rows:
        h = height[row[0]]
        print(max(row, key=len))
        complexity = len(max(row, key=len))
        if complexity==2:
            h = sum([height[l] for l in max(row, key=len)])
        mass = 0
        print(row)
        print(h)
        for block in row[1:]:
            print(float(block[0][1:]))
            delta(mode[block[0][0]], float(block[0][1:]), h, block[1], [coords[0]+mass,coords[1]], tang,skew_mode)
            mass+=float(block[0][1:])
        coords[1]-=h
        skew_mode = skew
    plt.show()
execute(file)

w, h = 10, 10
fig = plt.figure(frameon=True)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

L_height = 0.2
s_height = 0.06

m_sol = 330
m_nh3 = 0.5*200/22.4*(17)
m_co2 = 0.5*220/22.4*(12+16*2)
m_por = 75.44 + 184.88 + 258.85
m_nh3out = 116.74/2
m_przes = 64.81 + 162.22 + 231.36
m_prod = 47.682 + 69.86 + 79.71 - 42.58 - 57.37 - 63.11
coords = [0,0]
mass = m_sol

skew = (m_sol+m_nh3)/L_height*0.05
tang = 1.5*L_height/(m_nh3+m_sol)


delta(1, m_sol, L_height, 'solanka', coords, tang,0)
delta(1, m_nh3, L_height, 'NH$_3$', [coords[0]+m_sol, coords[1]], tang,0)
coords[1] -= L_height
m_wys = mass + m_nh3
delta(0, m_wys, s_height, 'wysycanie', coords, tang,0)
coords[1] -= s_height
delta(-1, m_nh3out, L_height, 'straty\nNH$_3$', coords, tang, skew)
coords[0] += m_nh3out
m_solam = mass+ m_nh3-m_nh3out
delta(0, m_solam, L_height, 'solanka amoniakalna', coords, tang,0)
delta(1, m_co2, L_height, 'CO$_2$', [coords[0]+m_solam, coords[1]], tang, skew)
coords[1] -= L_height
m_karb = mass+ m_nh3-m_nh3out+m_co2
delta(0, m_karb, s_height, 'karbonizacja', coords, tang,0)
coords[1] -= s_height
m_co2out = m_karb - m_por
delta(-1, m_co2out, L_height, 'straty\nCO$_2$', coords, tang, skew)
coords[0] += m_co2out
m_por = mass+ m_nh3-m_nh3out+m_co2-m_co2out
delta(0, m_por, L_height, 'mieszanina poreakcyjna', coords, tang,0)
coords[1] -= L_height
delta(0, m_por, s_height, 'sączenie pod zmniejszonym ciśnieniem', coords, tang,0)
coords[1] -= s_height
delta(-1, m_przes, L_height*2+s_height, 'przesącz', coords, tang, 0)
coords[0] += m_przes
m_mokr = mass+ m_nh3-m_nh3out+m_co2-m_co2out - m_przes
delta(0, m_mokr, L_height, 'soda\nmokra', coords, tang,0)
coords[1] -= L_height
delta(0, m_mokr, s_height, 'suszenie', coords, tang,0)
coords[1] -= s_height
m_wod = mass + m_nh3-m_nh3out+m_co2-m_co2out - m_przes- m_prod
delta(-1, m_wod, L_height, 'woda', coords, tang, 0)
coords[0] += m_wod
delta(-1, m_prod, L_height, 'bikarbonat', coords, tang, 0)

plt.show()