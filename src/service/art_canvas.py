class Canvas:
    width = 64
    height = 48

    centerX = width // 2
    centerY = height // 2

    left = 0
    right = width - 1
    top = 0
    bottom = height - 1

    def __init__(self):
        self._canvas = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def pixel(self, x, y, color = 1):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self._canvas[y][x] = color
    
    def get_pixel(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self._canvas[y][x]
        else:
            return 0
    
    def rect(self, x1, y1, x2, y2, color = 1):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self._canvas[y][x] = color
    
    def circle(self, x, y, r, color = 1):
        for px in range(x - r, x + r + 1):
            for py in range(y - r, y + r + 1):
                if (px - x) ** 2 + (py - y) ** 2 <= r ** 2:
                    self.pixel(px, py, color)
    
    def line(self, x1, y1, x2, y2, color = 1):
        # use Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                self.pixel(x, y, color)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                self.pixel(x, y, color)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        self.pixel(x, y, color)
    
    def _edgeCal(self, x1, y1, x2, y2, px, py):
        ax, ay = px - x1, py - y1
        bx, by = x2 - x1, y2 - y1

        return ax * by - ay * bx # cross product
    
    def triangle(self, x1, y1, x2, y2, x3, y3, color = 1):

        # use Barycentric coordinates
        # https://en.wikipedia.org/wiki/Barycentric_coordinate_system

        # find the bounding box
        xMin = min(x1, x2, x3)
        xMax = max(x1, x2, x3)
        yMin = min(y1, y2, y3)
        yMax = max(y1, y2, y3)

        for y in range(yMin, yMax + 1):
            for x in range(xMin, xMax + 1):
                w1 = self._edgeCal(x2, y2, x3, y3, x, y)
                w2 = self._edgeCal(x3, y3, x1, y1, x, y)
                w3 = self._edgeCal(x1, y1, x2, y2, x, y)

                if (w1 >= 0 and w2 >= 0 and w3 >= 0) or (w1 <= 0 and w2 <= 0 and w3 <= 0):
                    self.pixel(x, y, color)
    
    def flip(self, horizontal = False, vertical = False):
        if horizontal:
            for y in range(self.height):
                for x in range(self.width // 2):
                    self._canvas[y][x], self._canvas[y][self.width - x - 1] = self._canvas[y][self.width - x - 1], self._canvas[y][x]
        if vertical:
            for y in range(self.height // 2):
                self._canvas[y], self._canvas[self.height - y - 1] = self._canvas[self.height - y - 1], self._canvas[y]


    def convert_to_int32_array(self):
        int32Array = []
        for y in range(self.height):
            numByte = 0
            for x in range(self.width):
                calPos = self.width - x - 1
                numByte <<= 1
                if self._canvas[y][x] != 0:
                    numByte += 1
                
                if (calPos) % 32 == 0:
                    int32Array.append(numByte)
                    numByte = 0
        return int32Array

def extractType2(type, n_type1, n_type2):
    """ถอด type ออกมาเป็น 2 ตัว (type จาก 0 ถึง n_type - 1)"""
    return (type % n_type1, type // n_type1)

def extractType3(type, n_type1, n_type2, n_type3):
    """ถอด type ออกมาเป็น 3 ตัว (type จาก 0 ถึง n_type - 1)"""
    #return (type // (n_type2 * n_type3), (type // n_type3) % n_type2, type % n_type3)
    return (type % n_type1, (type // n_type1) % n_type2, type // (n_type1 * n_type2))

def extractType4(type, n_type1, n_type2, n_type3, n_type4):
    """ถอด type ออกมาเป็น 4 ตัว (type จาก 0 ถึง n_type - 1)"""
    return (type % n_type1, (type // n_type1) % n_type2, (type // (n_type1 * n_type2)) % n_type3, type // (n_type1 * n_type2 * n_type3))

def extractType5(type, n_type1, n_type2, n_type3, n_type4, n_type5):
    """ถอด type ออกมาเป็น 5 ตัว (type จาก 0 ถึง n_type - 1)"""
    return (type % n_type1, (type // n_type1) % n_type2, (type // (n_type1 * n_type2)) % n_type3, (type // (n_type1 * n_type2 * n_type3)) % n_type4, type // (n_type1 * n_type2 * n_type3 * n_type4))

def extractType6(type, n_type1, n_type2, n_type3, n_type4, n_type5, n_type6):
    """ถอด type ออกมาเป็น 6 ตัว (type จาก 0 ถึง n_type - 1)"""
    return (type % n_type1, (type // n_type1) % n_type2, (type // (n_type1 * n_type2)) % n_type3, (type // (n_type1 * n_type2 * n_type3)) % n_type4, (type // (n_type1 * n_type2 * n_type3 * n_type4)) % n_type5, type // (n_type1 * n_type2 * n_type3 * n_type4 * n_type5))