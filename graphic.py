import matplotlib.pyplot as plt
from numpy import sign

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
    ax.annotate(name, xy, ha='center', va='center').draggable()

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
m_nh3out = 30
m_przes = 64.81 + 162.22 + 231.36
m_prod = 47.682 + 69.86 + 79.71 - 42.58 - 57.37 - 63.11
coords = [0,0]
mass = m_sol

skew = (m_sol+m_nh3)/L_height*0.05
tang = 1.5*L_height/(m_nh3+m_sol)


delta(1, m_sol, L_height, 'solanka', coords, tang,0)
delta(1, m_nh3, L_height, 'NH3', [coords[0]+m_sol, coords[1]], tang,0)
coords[1] -= L_height
mass += m_nh3
delta(0, mass, s_height, 'wytrącanie', coords, tang,0)
coords[1] -= s_height
delta(-1, m_nh3out, L_height, 'straty\nNH$_3$', coords, tang, skew)
coords[0] += m_nh3out
mass -= m_nh3out
delta(0, mass, L_height, 'solanka amoniakalna', coords, tang,0)
delta(1, m_co2, L_height, 'CO$_2$', [coords[0]+mass, coords[1]], tang, skew)
coords[1] -= L_height
mass += m_co2
delta(0, mass, s_height, 'karbonizacja', coords, tang,0)
coords[1] -= s_height
m_co2out = mass - m_por
delta(-1, m_co2out, L_height, 'straty\nCO$_2$', coords, tang, skew)
coords[0] += m_co2out
mass -= m_co2out
delta(0, mass, L_height, 'mieszanina poreakcyjna', coords, tang,0)
coords[1] -= L_height
delta(0, mass, s_height, 'sączenie pod zmniejszonym ciśnieniem', coords, tang,0)
coords[1] -= s_height
delta(-1, m_przes, L_height*2+s_height, 'przesącz', coords, tang, 0)
coords[0] += m_przes
mass -= m_przes
delta(0, mass, L_height, 'soda\nmokra', coords, tang,0)
coords[1] -= L_height
delta(0, mass, s_height, 'suszenie', coords, tang,0)
coords[1] -= s_height
mass -= m_prod
delta(-1, mass, L_height, 'woda', coords, tang, 0)
coords[0] += mass
delta(-1, m_prod, L_height, 'bikarbonat', coords, tang, 0)
plt.show()