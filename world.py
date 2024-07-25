#
# Stupidly simple three-D projection
#

import pygame
import math

class World:
  # Coordinates are north, east, up (in metres)
  # World is a list of objects, where each object is an (R, G, B) colour triplet,
  # followed by a list of points in (N, E, U) format
  # Each object is drawn with a vector connecting each pair of points in the object
  world = []
  worlddots = []
  polygons = []

  sin_roll  = 0.0
  cos_roll  = 1.0
  sin_pitch = 0.0
  cos_pitch = 1.0
  sin_hdg   = 0.0
  cos_hdg   = 1.0
  zoom      = 1.0

  focal_plane = 1.0

  # 3D coordinates of last point successfully projected
  last_x     = 0.0
  last_y     = 0.0
  last_z     = 0.0

  # True if last point projected was inside frustrum, False otherwise
  inside = True

  # Bunch of RGB colours
  sky_blue  = (135, 206, 235)
  lake_blue = (0x5e, 0x8f, 0xc7)
  grass_grn = (72, 111, 56)
  wht_stripe= (200, 200, 200)
  dark_gray = (50, 50, 50)
  black     = (0, 0, 0)

  # Rotate point x,y by hdg radians and translate to origin n,e
  def rotate_translate_pt(self, n, e, hdg, x, y):
    nn = (x * math.cos(hdg) - y * math.sin(hdg)) + n
    ee = (x * math.sin(hdg) + y * math.cos(hdg)) + e
    #print(f"x={x:f} y={y:f} nn={nn:f} ee={ee:f}")
    return (nn, ee, 0)

  # Make a runway out of lots of little segments
  # With a dashed centre line
  def make_runway(self, length, n, e, orient):
    w = 75  # Width
    s = 100 # Len of segment
    sl = 40 # Len of stripe
    numsegs = int(round(length/s)) # Number of segments
    numstripes = int(round(length/sl)) # Number of stripes
    r = []  # Runway outline
    p = []  # Polygons

    r.append(self.wht_stripe) # Colour is first element
    # Runway outline
    for i in range(0, numsegs):
      r.append(self.rotate_translate_pt(n, e, orient, i*s, -w/2))
    r.append(self.rotate_translate_pt(n, e, orient, i*s, w/2))
    for i in range(0, numsegs):
      r.append(self.rotate_translate_pt(n, e, orient, (numsegs-1-i)*s, w/2))
    r.append(self.rotate_translate_pt(n, e, orient, 0, -w/2))

    # Polygon fill
    for i in range(0, numsegs):
      poly = []
      poly.append(self.dark_gray) # First element is the colour
      poly.append(self.rotate_translate_pt(n, e, orient, i*s, -w/2))
      poly.append(self.rotate_translate_pt(n, e, orient, (i+1)*s, -w/2))
      poly.append(self.rotate_translate_pt(n, e, orient, (i+1)*s, w/2))
      poly.append(self.rotate_translate_pt(n, e, orient, i*s, w/2))
      poly.append(self.rotate_translate_pt(n, e, orient, i*s, -w/2))
      p.append(poly)

    # Centreline stripes as polygons
    for i in range(0, numstripes):
      stripe = []
      stripe.append(self.wht_stripe) # First element is the colour
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.25), -0.5))
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.75), -0.5))
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.75), +0.5))
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.25), +0.5))
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.25), -0.5))
      stripe.append(self.rotate_translate_pt(n, e, orient, i*sl+(sl*.25), -0.5))
      p.append(stripe)

    return ([r], p)

  # Make a little house
  def make_building(self,x,y,sz,h):
    cube   = [self.black,
              (x+0, y+0, 0), (x+sz, y+0, 0), (x+sz, y+sz, 0), (x+0, y+sz, 0), (x+0, y+0, 0),
              (x+0, y+0, h), (x+sz, y+0, h), (x+sz, y+sz, h), (x+0, y+sz, h), (x+0, y+0, h)]
    l1 = [self.black, (x+sz, y+0, 0), (x+sz, y+0, h)]
    l2 = [self.black, (x+sz, y+sz, 0), (x+sz, y+sz, h)]
    l3 = [self.black, (x+0, y+sz, 0), (x+0, y+sz, h)]
    return [cube, l1, l2, l3]
   
  # Make some area polygons
  def make_polygons(self):
    p1 = [self.lake_blue, (-1500, 0, 0), (-1500, 200, 0), (-1400, 300, 0), (-1300, 200, 0), (-1300, 0, 0), (-1400, -100, 0)] # Little lake
    p2 = [self.lake_blue, (-2500, -5000, 0), (+2500, -5000, 0), (+2500, -7500, 0), (-2500, -7500, 0)] # Big lake
    return [p1, p2]

  # Update the camera angle
  # roll,pitch,hdg is camera angle
  # zoom is the distance to the projection plane
  def update_view(self, roll, pitch, hdg, zoom):
    self.sin_roll  = math.sin(-roll)
    self.cos_roll  = math.cos(-roll)
    self.sin_pitch = math.sin(-pitch)
    self.cos_pitch = math.cos(-pitch)
    self.sin_hdg   = math.sin(hdg)
    self.cos_hdg   = math.cos(hdg)
    self.zoom      = zoom

  # x,y,z are 3D world coordinates of point to project
  # north,east,alt is camera pos
  def project_point(self, x, y, z, north, east, alt, horizon = False):

    alt += 3 # Viewpoint above the ground

    if horizon == False:

      # Translate camera position
      x -= north
      y -= east
      z -= alt

      # Rotation around z-axis (heading)
      x_z = x * self.cos_hdg - y * self.sin_hdg
      y_z = x * self.sin_hdg + y * self.cos_hdg
      z_z = z

    else:
      # If drawing horizon, no translation for position,
      # or rotation for heading
      z -= alt
      x_z = x
      y_z = y
      z_z = z

    # Rotation around y-axis (pitch)
    x_zy = x_z * self.cos_pitch + z_z * self.sin_pitch
    y_zy = y_z
    z_zy = -x_z * self.sin_pitch + z_z * self.cos_pitch

    # Rotation around x-axis (roll)
    x_zyx = x_zy
    y_zyx = y_zy * self.cos_roll - z_zy * self.sin_roll
    z_zyx = y_zy * self.sin_roll + z_zy * self.cos_roll

    if x_zyx > self.focal_plane:
      # Point is within the frustrum
      # Store the 3D coordinates of successfully-projected point
      self.last_x = x_zyx
      self.last_y = y_zyx
      self.last_z = z_zyx
      self.inside = True
      return (self.zoom * y_zyx / x_zyx, self.zoom * z_zyx / x_zyx)
    else:
      # Point is closer to viewer than the focal plane
      if self.inside == False:
        # Previous point was also outside frustrum
        self.last_x = x_zyx
        self.last_y = y_zyx
        self.last_z = z_zyx
        return -1
      else:
        # Previous point was inside frustrum
        p = self.clip_to_focal_plane(x_zyx, y_zyx, z_zyx, leaving=True)
        self.last_x = x_zyx
        self.last_y = y_zyx
        self.last_z = z_zyx
        return p

  # Compute the intersection of line from (self.last_x,self.last_y,self.last_z)
  # to (x_zyx,y_zyx,z_zyx) with the focal plane.
  def clip_to_focal_plane(self, x_zyx, y_zyx, z_zyx, leaving=True):
    delta_x = x_zyx - self.last_x
    delta_y = y_zyx - self.last_y
    delta_z = z_zyx - self.last_z
    ratio = (self.focal_plane - self.last_x) / delta_x
    x_zyx = self.last_x + ratio * delta_x
    y_zyx = self.last_y + ratio * delta_y
    z_zyx = self.last_z + ratio * delta_z
    self.inside = not leaving
    return (self.zoom * y_zyx / x_zyx, self.zoom * z_zyx / x_zyx)

  # Draw polygon where one side is from pt1->pt2 and other side is parallel
  # at a distance of h pixels.  Used for filling ground and sky.
  def sky_and_ground(self, pt1, pt2, sky, colour):
    if sky == True:
      h = 10000
    else:
      h = -10000
    (x1, y1) = pt1
    (x2, y2) = pt2
    opp = y2 - y1
    adj = x2 - x1
    hyp = math.sqrt(opp * opp + adj * adj)
    x1 += self.middle_x
    x2 += self.middle_x
    y1 = self.middle_y - y1
    y2 = self.middle_y - y2
    x3 = x1 - h * opp / hyp
    x4 = x2 - h * opp / hyp
    y3 = y1 - h * adj / hyp
    y4 = y2 - h * adj / hyp
    pygame.draw.polygon(self.imgbuf, colour, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])
  
  # Utility function used for drawing lines
  # Params: colour is the RGB colour
  #         pt1, pt2 are (x,y) coordinates for endpoints
  def drawline(self, colour, pt1, pt2):
    (x1, y1) = pt1
    (x2, y2) = pt2
    x1 += self.middle_x
    x2 += self.middle_x
    y1 = self.middle_y - y1
    y2 = self.middle_y - y2
    pygame.draw.line(self.imgbuf, colour, (x1, y1), (x2, y2))

  # Draw the whole world
  # north,east,alt is camera pos
  # roll,pitch,hdg is camera angle
  # zoom is the distance to the projection plane
  # viewangle is direction of view in degrees
  def show(self, north, east, alt, roll, pitch, hdg, zoom, viewangle):
    if viewangle == 45:
      self.update_view(roll, pitch, hdg-math.pi*0.25, zoom)
    elif viewangle == 90:
      self.update_view(pitch, -roll, hdg-math.pi*0.5, zoom)
    elif viewangle == 135:
      self.update_view(-roll, -pitch, hdg-math.pi*0.75, zoom)
    elif viewangle == 180:
      self.update_view(-roll, -pitch, hdg-math.pi, zoom)
    elif viewangle == -135:
      self.update_view(-roll, -pitch, hdg+math.pi*0.75, zoom)
    elif viewangle == -90:
      self.update_view(-pitch, roll, hdg+math.pi/2, zoom)
    elif viewangle == -45:
      self.update_view(roll, pitch, hdg+math.pi*0.25, zoom)
    else:
      self.update_view(roll, pitch, hdg, zoom)

#   pygame.draw.rect(self.imgbuf, (0, 0, 0), self.rect) # Erase

    # Horizon line
    pt1 = self.project_point(100000, -100000, 0.0, north, east, alt, horizon = True)
    pt2 = self.project_point(100000, +100000, 0.0, north, east, alt, horizon = True)
    if pt1 != -1 and pt2 != -1:
      self.sky_and_ground(pt1, pt2, sky=True,  colour=self.sky_blue)  # Sky
      self.sky_and_ground(pt1, pt2, sky=False, colour=self.grass_grn) # Ground
   
    for poly in self.polygons:
      ptlist = []
      self.inside = False
      counter = 0
      first = True
      for vertex in poly:
        if counter == 0:
          # First element of the list is the colour
          colour = vertex
        else:
          (n, e, u) = vertex
          prev_inside = self.inside
          old_last_x = self.last_x
          old_last_y = self.last_y
          old_last_z = self.last_z
          pt = self.project_point(n, e, u, north, east, alt)
          if pt != -1:
            (x, y) = pt
            pt =  (x + self.middle_x, self.middle_y - y)
          if counter == 1 and self.inside == True:
            # First point of shape
            if self.inside == True:
              ptlist.append(pt)
          elif self.inside == True and prev_inside == True:
            # Line entirely within frustrum - normal draw
            ptlist.append(pt)
          elif self.inside == True and prev_inside == False:
            # Line entering the frustrum - need to add extra point
            (x, y) = self.clip_to_focal_plane(old_last_x, old_last_y, old_last_z, leaving=False)
            ptlist.append((x + self.middle_x, self.middle_y - y))
            ptlist.append(pt)
          elif self.inside == False and prev_inside == True:
            # Line leaving the frustrum - normal draw
            ptlist.append(pt)
          else:
            # Line entirely outside of frustrum - don't draw
            pass
        counter += 1
      if len(ptlist) > 2:
        pygame.draw.polygon(self.imgbuf, colour, ptlist)

    for obj in self.world:
      prev_pt = -1
      self.inside = False
      counter = 0
      first = True
      for vertex in obj:
        if counter == 0:
          # First element of the list is the colour
          colour = vertex
        else:
          (n, e, u) = vertex
          prev_inside = self.inside
          old_last_x = self.last_x
          old_last_y = self.last_y
          old_last_z = self.last_z
          pt = self.project_point(n, e, u, north, east, alt)
          if counter == 1:
            # First point of shape (which can be -1 if it lies outside frustrum)
            prev_pt = pt
          elif self.inside == True and prev_inside == True:
            # Line entirely within frustrum - normal draw
            self.drawline(colour, prev_pt, pt)
            prev_pt = pt
          elif self.inside == True and prev_inside == False:
            # Line entering the frustrum - need to clip to compute prev_pt
            prev_pt = self.clip_to_focal_plane(old_last_x, old_last_y, old_last_z, leaving=False)
            self.drawline(colour, prev_pt, pt)
            prev_pt = pt
          elif self.inside == False and prev_inside == True:
            # Line leaving the frustrum - clipping is handled already in project_point()
            self.drawline(colour, prev_pt, pt)
            prev_pt = pt
          else:
            # Line entirely outside of frustrum - don't draw
            pass
        counter += 1

    for dot in self.worlddots:
      (n, e, u) = dot
      pt = self.project_point(n, e, u, north, east, alt)
      if pt != -1:
        (x, y) = pt
        x += self.middle_x
        y = self.middle_y - y
        self.imgbuf.set_at((int(x), int(y)), (255, 255, 255))
    self.display.blit(self.imgbuf, (self.ox, self.oy), (0, 0, self.sx, self.sy))
    pygame.display.update()

  # Build the world!
  def __init__(self, display, offset, size):
    (l, p) = self.make_runway(3000, 0, 0, orient=0.00)
    self.world = l
    self.polygons = self.make_polygons()
    self.polygons += p
    (l, p) = self.make_runway(3000, 0, -1500, orient=math.pi/4)
    self.world += l
    self.polygons += p
    (l, p) = self.make_runway(2000, 5000, 7500, orient=math.pi)
    self.world += l
    self.polygons += p
    (l, p) = self.make_runway(2000, -5000, 2500, orient=math.pi/8)
    self.world += l
    self.polygons += p
    for i in range(1,6):
      self.world += self.make_building(200+i*200,150,50,30)
    self.world += self.make_building(-2000,-2000,100,750) # Skyscraper
    self.display = display
    self.imgbuf = pygame.Surface(size)
    (self.ox, self.oy) = offset
    (self.sx, self.sy) = size
    self.middle_x = self.sx/2
    self.middle_y = self.sy/2
    self.rect = pygame.Rect(0, 0, self.sx, self.sy)

    return # BAIL EARLY
    # Draw ground grid as dots
    gridsize = 40000 # Total extent of grid is (gridsize*2)^2
    gridint1 = 200   # Minor spacing
    gridint2 = 2000  # Major spacing
    north_min = -gridsize
    north_max = +gridsize
    east_min  = -gridsize
    east_max  = +gridsize
    for n in range(north_min, north_max, gridint2):
      for e in range(east_min, east_max, gridint1):
        self.worlddots.append((n, e, 0))
    for e in range(east_min, east_max, gridint2):
      for n in range(north_min, north_max, gridint1):
        self.worlddots.append((n, e, 0))


