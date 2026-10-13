import json
rows=json.load(open('cell/trace.json'))['rows']
S=0.1634; CX=499.5; Y0=194
# symmetric half-width profile: average left/right and top/bottom mirror
def hw(y):
    L,R=rows[y]; return (R-L)/2
ys=[194,195,196,198,200,203,206,210,215,222,232,246,264,290,330,380,440,500]
pts=[]
for y in ys:
    ym=1000-y  # mirror (806 ~ 194)
    h=(hw(y)+hw(min(ym,806)))/2 if rows[min(ym,806)][0]>=0 else hw(y)
    pts.append(((y-Y0)*S, h*S))
top=pts  # y from 0 to 50
# full contour clockwise from top center: right side top->bottom, then left side bottom->top
right=[(30+h,y) for y,h in top]+[(30+h,100-y) for y,h in reversed(top[:-1])]
left=[(30-h,y) for (x,y) in [(0,0)] for _ in []]
contour=[(30, 0.0)]+right[1:]  # starting at top center
# right side ends at bottom (y=100). add left side
left=[(60-x,y) for x,y in reversed(right[:-1])]
contour=right+left[1:]
# close: contour starts at (30+h0,0)
def cr(points):
    n=len(points); d=f"M{points[0][0]:.2f} {points[0][1]:.2f}"
    for i in range(n):
        p0=points[(i-1)%n]; p1=points[i]; p2=points[(i+1)%n]; p3=points[(i+2)%n]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f"C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f}"
    return d+"Z"
path=cr(contour)
open('cell/outer.txt','w').write(path)
print(len(contour), len(path)); print(path[:400])
for y,h in top: print(round(y,2), round(h,2))
