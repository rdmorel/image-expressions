from Myro import *
from Graphics import *

def brightness(px):
    ''' find the brightness of a pixel'''
    return sum(getRGB(px))/3

class BPicture(Picture):

    def __init__(self, p):
        Picture.__init__(self)
        
    def __and__(self, other):
        '''min: makes all pixels the min value of RGB of the two pictures
        When combined with a black & white photo, just puts the
        black of the b&w photo over the color photo.'''
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            opx = getPixel(other, x, y)
            setRed(px, min(getRed(px), getRed(opx)))
            setGreen(px, min(getGreen(px), getGreen(opx)))
            setBlue(px, min(getBlue(px), getBlue(opx)))
            #print(getRed(opx), getRed(px))

        return newImage


    def __rshift__(self, amount):
        '''shift: shifts all pixels right
        works the same no matter the image color.'''
        newImage = BPicture(copyPicture(self))
        w = getWidth(newImage)

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            if 0 < x - amount < w:
                setColor(px, getColor(self, x - amount, y))
            else:
                setColor(px, Color('black'))
  
        return newImage

    def __lshift__(self, amount):
        '''shift: shifts all pixels left
        works the same no matter the image color.'''
        return self.__rshift__(-amount)
    
    def __pos__(self):
        ''' dilate: expand the bright pixels
        has interesting effects on black & white pics,
        making white parts bigger'''
        w = getWidth(self)
        h = getHeight(self)
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            value = brightness(px)
            color = getColor(px)
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        opx = getPixel(self, x + dx, y + dy)
                        if value < brightness(opx):
                            value = brightness(opx)
                            color = getColor(opx)        
            setColor(px, color)
            
        return newImage
    
    def __neg__(self):
        ''' erode: enlarge the dark pixels
        has interesting effects on black & white pics,
        making black parts bigger'''
        w = getWidth(self)
        h = getHeight(self)
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            value = brightness(px)
            color = getColor(px)
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        opx = getPixel(self, x + dx, y + dy)
                        if value > brightness(opx):
                            value = brightness(opx)
                            color = getColor(opx)        
            setColor(px, color)

        return newImage

    def __invert__ (self):
        '''inverts the color of the picture
        inversion looks a lot less scary when
        the image is black and white. Color pictures
        make things look like ghosts.'''
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            setRed(px, 255-getRed(px))
            setGreen(px, 255-getGreen(px))
            setBlue(px, 255-getBlue(px))

        return newImage

    def __or__ (self,other):
        '''max: takes the max RGB of two pictures for each pixel
        can overlap images, and when using a black & white pic
        combined with a color picture, it basically keeps the
        white of the b&w picture and fills the black spaces with
        whatever the color picture looked like.'''
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            opx = getPixel(other, x, y)
            setRed(px, max(getRed(px), getRed(opx)))
            setGreen(px, max(getGreen(px), getGreen(opx)))
            setBlue(px, max(getBlue(px), getBlue(opx)))

        return newImage

    def __xor__ (self, other):
        '''abs: takes absolute value of difference between pixel brightness
        When using a b&w photo with a color photo, the sections of the
        b&w photo that are black appear like the regular color photo
        with no effects.'''
        w = getWidth(self)
        h = getHeight(self)
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            opx = getPixel(other, x, y)
            setRed(px, abs(getRed(px) - getRed(opx)))
            setGreen(px, abs(getGreen(px) - getGreen(opx)))
            setBlue(px, abs(getBlue(px) - getBlue(opx)))

        return newImage

    def __gt__ (self, threshold):
        '''threshold: sets all pixels with brightness > threshold white, and the rest black
        basically makes any picture black & white. If used on a
        grayscale picture, it makes the difference between black
        and white really harsh.'''
        w = getWidth(self)
        h = getHeight(self)
        newImage = BPicture(copyPicture(self))

        for px in getPixels(newImage):
            x = getX(px)
            y = getY(px)
            if brightness(px) > threshold:
                setRed(px, 255)
                setGreen(px, 255)
                setBlue(px, 255)
            else:
                setRed(px, 0)
                setGreen(px, 0)
                setBlue(px, 0)

        return newImage

a = BPicture(makePicture("dogtest.jpg"))
b = BPicture(makePicture("appletest.jpg"))
c = BPicture(makePicture("bwtest.jpg"))

def test():
    ask("Press enter")
    bg = BPicture(takePicture())
    ask("Press enter again")
    fg = BPicture(takePicture())

    show(bg ^ fg)
    show((bg ^ fg) > 20)
    show(++--((bg ^ fg) > 20))
    show((++--((bg ^ fg) > 20))^+(++--((bg^fg)>20)))
    show(~(+-((bg^fg) > 20 ) >> 75) & bg)
    show(~(+-((bg^fg) > 20 ) >> 75) & bg | ((+-((bg^fg)>20) &fg)>>75))
