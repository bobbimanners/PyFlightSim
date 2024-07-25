#!/usr/bin/python3

#
# Primary flight display
# Bobbi Webber-Manners
# June 2024
#

import math
import pygame
import convert

# Primary flight display (PFD)
class PFD:

  # Initialize graphics for PFD
  def __init__(self, display, offset, size):
    self.display = display
    self.offset  = offset
    (sx, sy)     = size
    self.xscale  = sx / 800 # Used for rescaling UI
    self.yscale  = sy / 700 # Used for rescaling UI
    self.size    = size
    
    self.font32  = pygame.font.Font('freesansbold.ttf', self.rescale_y(32))
    self.font24  = pygame.font.Font('freesansbold.ttf', self.rescale_y(24))
    self.font16  = pygame.font.Font('freesansbold.ttf', self.rescale_y(16))
    self.black   = (0,0,0)
    self.white   = (255,255,255)
    self.grey    = (128,128,128)
    self.brown   = (0x98,0x76,0x54)
    self.blue    = (0x95,0xcb,0xdb)
    self.magenta = (255,0,255)
    self.red     = (255,0,0)
    self.yellow  = (255,255,0)
    self.pfdimgbuf = pygame.Surface(size)

  def rescale_x(self, pixels):
    return int(round(pixels * self.xscale))

  def rescale_y(self, pixels):
    return int(round(pixels * self.yscale))

  # Draw compass rose with yaw rate arc above
  def draw_rose(self, yaw_d):
    (w, h) = self.size
    centx = w / 2          # Centre of compass rose - x
    centy = w * 11/7       # Centre of compass rose - y
    radius = w * 5/8       # Radius of compass rose
    trradius = radius + self.rescale_x(10) # Radius of turn rate trend arc
    arcwidth = self.rescale_x(5)
  
    # Yaw rate arc
    if yaw_d > 0.0:
      pygame.draw.arc(self.pfdimgbuf, self.magenta,
                      (centx-trradius, centy-trradius, 2*trradius, 2*trradius),
                      math.pi/2-yaw_d, math.pi/2, width=arcwidth)
    else:
      pygame.draw.arc(self.pfdimgbuf, self.magenta,
                      (centx-trradius, centy-trradius, 2*trradius, 2*trradius),
                      math.pi/2, math.pi/2-yaw_d, width=arcwidth)

    pygame.draw.line(self.pfdimgbuf, self.white,
                     (centx, centy-trradius-self.rescale_y(25)),
                     (centx, centy-trradius+self.rescale_y(10)), self.rescale_x(7))
  
    # Compass rose
    pygame.draw.circle(self.pfdimgbuf, self.grey, (centx, centy), radius, 0)
    for h in range(0, 36):
  
      a = convert.degtorad(h * 10) - self.hdg
      inner_rad = 0.9 if ((h % 2) == 1) else 0.975
      x1 = centx + radius * inner_rad * math.sin(a)
      y1 = centy - radius * inner_rad * math.cos(a)
      x2 = centx + radius * 1.0 * math.sin(a)
      y2 = centy - radius * 1.0 * math.cos(a)
      xt = centx + radius * 0.9 * math.sin(a)
      yt = centy - radius * 0.9 * math.cos(a)
      pygame.draw.line(self.pfdimgbuf, self.white, (x1, y1), (x2, y2), 3)
  
      if h == 0:
        t = 'N'
      elif h == 9:
        t = 'E'
      elif h == 18:
        t = 'S'
      elif h == 27:
        t = 'W'
      else:
        t = f"{h:d}"
  
      if t != "":
        text = self.font32.render(t, True, self.white, self.grey)
        rtext = pygame.transform.rotate(text, -convert.radtodeg(a))
        textRect = rtext.get_rect()
        textRect.center = (xt, yt)
        self.pfdimgbuf.blit(rtext, textRect)
  
    text = self.font24.render(f"{int(convert.radtodeg(self.hdg)):03d}\u00b0",
                              True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, self.rescale_y(575))
    self.pfdimgbuf.blit(text, textRect)
  
  # Draw pitch lines on PFD
  # Params: pl - pitch for pitch line in degrees
  #         l - length of pitch line
  #         withtext - if True, label the line
  def draw_pitchline(self, pl, l, withtext):
    (w, h) = self.size
    pl_vert_px = (pl + convert.radtodeg(self.pitch)) * self.rescale_y(10)
    hcent = w/2 + pl_vert_px * math.sin(self.roll)
    vcent = h/2 + pl_vert_px * math.cos(self.roll)
    x1 = hcent - l/2 * math.cos(self.roll)
    x2 = hcent + l/2 * math.cos(self.roll)
    y1 = vcent + l/2 * math.sin(self.roll)
    y2 = vcent - l/2 * math.sin(self.roll)
    pygame.draw.line(self.pfdimgbuf, self.white, (x1, y1), (x2, y2), self.rescale_y(2))
    if (withtext and pl != 0):
      text = self.font24.render(f"{int(math.fabs(pl)):2d}",
                                True, self.white, self.blue if pl < 0 else self.brown)
      rtext = pygame.transform.rotate(text, convert.radtodeg(self.roll))
      textRect = rtext.get_rect()
      textRect.center = (x2, y2)
      self.pfdimgbuf.blit(rtext, textRect)
  
  # Draw PFD.  Main entry point.
  def draw(self, roll, pitch, hdg, yaw_d, x_d, z_world, z_d_world,
           aileron, elevator, rudder, throttle, autorudder, y_dd, alpha):
    (w, h) = self.size
    h *= 6/7 # Leave space for compass rose at bottom

    self.roll     = roll
    self.pitch    = pitch
    self.hdg      = hdg
    self.sideslip = y_dd

    # Rescale fixed-sized elements
    r5 = self.rescale_y(5)
    r6 = self.rescale_y(6)
    r8 = self.rescale_y(8)
    r10 = self.rescale_y(10)
    r15 = self.rescale_y(15)
    r20 = self.rescale_y(20)
    r25 = self.rescale_y(25)
    r30 = self.rescale_y(30)
    r50 = self.rescale_y(50)
    r70 = self.rescale_y(70)
    r75 = self.rescale_y(75)
    r100 = self.rescale_y(100)
    r150 = self.rescale_y(150)
    r200 = self.rescale_y(200)
    r300 = self.rescale_y(300)
    r565 = self.rescale_y(565)
    r615 = self.rescale_y(615)
  
    # Artificial horizon
    vert_px = (convert.radtodeg(pitch)) * r10
    hcent = w/2 + vert_px * math.sin(roll)
    vcent = h/2 + vert_px * math.cos(roll)
    x1 = hcent - w/2 * math.cos(roll)
    x2 = hcent + w/2 * math.cos(roll)
    y1 = vcent + w/2 * math.sin(roll)
    y2 = vcent - w/2 * math.sin(roll)
    vert_px = (convert.radtodeg(pitch) - 100) * r10
    hcent = w/2 + vert_px * math.sin(roll)
    vcent = h/2 + vert_px * math.cos(roll)
    x3 = hcent - w/2 * math.cos(roll)
    x4 = hcent + w/2 * math.cos(roll)
    y3 = vcent + w/2 * math.sin(roll)
    y4 = vcent - w/2 * math.sin(roll)
    pygame.draw.polygon(self.pfdimgbuf, self.blue, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])
    vert_px = (convert.radtodeg(pitch) + 100) * r10
    hcent = w/2 + vert_px * math.sin(roll)
    vcent = h/2 + vert_px * math.cos(roll)
    x3 = hcent - w/2 * math.cos(roll)
    x4 = hcent + w/2 * math.cos(roll)
    y3 = vcent + w/2 * math.sin(roll)
    y4 = vcent - w/2 * math.sin(roll)
    pygame.draw.polygon(self.pfdimgbuf, self.brown, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])

    # Pitch graticule
    for pl in range(-8, 8):
      self.draw_pitchline(pl * 10,       r200, True)
      self.draw_pitchline(pl * 10 + 2.5, r50,  False)
      self.draw_pitchline(pl * 10 + 5,   r75,  False)
      self.draw_pitchline(pl * 10 + 7.5, r50,  False)
   
    # Airplane symbol 
    pygame.draw.line(self.pfdimgbuf, self.yellow, (r200, h/2), (r300, h/2), r8)
    pygame.draw.line(self.pfdimgbuf, self.yellow, (w-r300, h/2), (w-r200, h/2), r8)
    pygame.draw.line(self.pfdimgbuf, self.yellow, (w/2-r50, h/2+r20), (w/2, h/2), r6)
    pygame.draw.line(self.pfdimgbuf, self.yellow, (w/2+r50, h/2+r20), (w/2, h/2), r6)
 
    # Black border 
    pygame.draw.rect(self.pfdimgbuf, self.black, (0, 0, w, r50))
    pygame.draw.rect(self.pfdimgbuf, self.black, (0, h-r50, w, r50+r100))
    pygame.draw.rect(self.pfdimgbuf, self.black, (0, 0, r50, h))
    pygame.draw.rect(self.pfdimgbuf, self.black, (w-r50, 0, r50, h))
  
    # ASI, altimeter, rate of climb
    text = self.font32.render(f"{int(convert.speedtoknots(x_d)):03d}",
                              True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (r50, h/2)
    self.pfdimgbuf.blit(text, textRect)
    text = self.font32.render(f"{int(convert.metrestofeet(z_world)):05d}",
                              True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (w-r50, h/2)
    self.pfdimgbuf.blit(text, textRect)
    for roc in range (1, 4):
      roc_len = roc * h/2 / 5
      text = self.font24.render(f"{-roc:+1d}", True, self.red, self.black)
      textRect = text.get_rect()
      textRect.center = (w-r20, h/2+r15 + roc_len)
      self.pfdimgbuf.blit(text, textRect)
      pygame.draw.line(self.pfdimgbuf, self.red,
                       (w-r70, h/2+r15+roc_len), (w-r30,h/2+r15+roc_len), 1)
      text = self.font24.render(f"{roc:+1d}", True, self.red, self.black)
      textRect = text.get_rect()
      textRect.center = (w-r20, h/2-r15 - roc_len)
      self.pfdimgbuf.blit(text, textRect)
      pygame.draw.line(self.pfdimgbuf, self.red,
                       (w-r70, h/2-r15-roc_len), (w-r30, h/2-r15-roc_len), 1)
    roc_len = convert.speedtofeetpermin(z_d_world) * h/2 / 5000
    if (roc_len > 0):
      pygame.draw.rect(self.pfdimgbuf, self.red, (w-r50, h/2-r15-roc_len, r20, roc_len))
    else:
      pygame.draw.rect(self.pfdimgbuf, self.red, (w-r50, h/2+r15, r20, -roc_len))
  
    # Control positions
    pygame.draw.rect(self.pfdimgbuf, self.red, (r50, r565, r100, r100), 1)
    pygame.draw.circle(self.pfdimgbuf, self.red,
                       (r100+r50*aileron, r615+r50*elevator), r5)
    pygame.draw.circle(self.pfdimgbuf, self.red,
                       (r100+r50*rudder, r565+r100), r5, 1 if autorudder == True else 0)
    pygame.draw.circle(self.pfdimgbuf, self.yellow, (r150, r565+r100-throttle*r100), r5)
  
    # Sideslip
    pygame.draw.line(self.pfdimgbuf, self.red, (w/2, r25), (w/2, r50), 3)
    pygame.draw.circle(self.pfdimgbuf, self.red, (w/2 + self.sideslip * r50, r25), r10)
  
    # Angle of attack
    text = self.font24.render(f"\u03b1={convert.radtodeg(alpha):+0.1f}\u00b0", True, self.magenta, self.black)
    textRect = text.get_rect()
    textRect.center = (50, 20)
    self.pfdimgbuf.blit(text, textRect)
    
    self.draw_rose(yaw_d)
 
    (sx, sy) = self.size 
    self.display.blit(self.pfdimgbuf, self.offset, (0, 0, sx, sy)) # Blit buffer to real display
    pygame.display.flip()
  
  
