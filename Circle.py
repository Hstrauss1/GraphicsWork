from PIL import Image

def anger(xc, yc, rad):
    border_pixels = {}
    def add_border_pixel(x, y):
        border_pixels[(xc + x, yc + y)] = True
        border_pixels[(xc - x, yc + y)] = True
        border_pixels[(xc + x, yc - y)] = True
        border_pixels[(xc - x, yc - y)] = True
        border_pixels[(xc + y, yc + x)] = True
        border_pixels[(xc - y, yc + x)] = True
        border_pixels[(xc + y, yc - x)] = True
        border_pixels[(xc - y, yc - x)] = True
    x = 0
    y = rad
    d = 1 - rad
    add_border_pixel(x, y) 
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        add_border_pixel(x, y)
    return border_pixels

#anti-ail helper functions
def blend(c1,c2, intensity):
    return tuple(int(c1[i] * intensity + c2[i] * (1 - intensity)) for i in range(3))
def intensity(x,y,rad):
    d = abs(x * x + y * y - rad * rad)
    return 1 - d / rad ** 2

#fill/reflect functions
def fill(pix, xl, xr, y, c):
        for x in range(xl, xr + 1):
            if (x, y) in border_pixels:
                pix[x, y] = blend(c,(0,0,0),0.4)
            elif (x,y) in bord2:
                pix[x, y] = blend(c,(0,0,0),0.8)
            elif (x,y) in bord3:
                pix[x, y] = blend(c,(0,0,0),0.95)
            else:
                pix[x, y] = c
def reflectPix(pix, xc, yc, x, y, c):
    fill(pix, xc - x, xc + x, yc + y, c)  
    fill(pix, xc - x, xc + x, yc - y, c) 
    fill(pix, xc - y, xc + y, yc + x, c) 
    fill(pix, xc - y, xc + y, yc - x, c)

#CircleFunction
def circleAlg(pix, xc, yc, c, rad):
    x = 0
    y = rad
    d = 1 - rad  #p0
    # Plot symmetric and fill
    reflectPix(pix, xc, yc, x, y, c)
    while x < y:
        if d < 0:#move right
            d += 2 * x + 3
        else:#move diagonally
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        reflectPix(pix, xc, yc, x, y, c)

bord2={}
bord3={}
border_pixels={}
def initiate():
    global bord2, bord3, border_pixels
    xsize=input("what x size")
    ysize=input("what y size")
    xsize,ysize=int(xsize),int(ysize)
    img = Image.new('RGB', (xsize, ysize))
    pix = img.load()
    xloc=input("what x location is the center")
    yloc=input("what x location is the center")
    xloc,yloc=int(xloc),int(yloc)
    radius=input("what radius do you want the circle")
    radius=int(radius)
    bord3=anger(xloc,yloc,radius-2)
    bord2=anger(xloc,yloc,radius-1)
    border_pixels = anger(xloc, yloc, radius)
    circleAlg(pix,xloc,yloc,(0,166,166),radius)
    large_size = (xsize * 3, ysize * 3)
    img_large = img.resize(large_size, Image.NEAREST)  # resize up to a larger size
    
    img_anti_aliased = img_large.resize((xsize, ysize), Image.LANCZOS)  # resize back down with LANCZOS filter
    
    # Show the anti-aliased image
    img_anti_aliased.show()


initiate()
