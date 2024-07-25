#
# Steam panel
# Bobbi Webber-Manners
# July 2024
#

import math
import pygame
import convert

# Steam panel
class Steam:

  # Initialize graphics for steam panel
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
    self.green   = (0,255,0)
    self.imgbuf  = pygame.Surface(size)

  def rescale_x(self, pixels):
    return int(round(pixels * self.xscale))

  def rescale_y(self, pixels):
    return int(round(pixels * self.yscale))

  # Draw compass rose
  def draw_rose(self, x, y, size):
    (ww, hh) = size
    centx = x + ww / 2   # Centre of compass rose - x
    centy = y + hh / 2   # Centre of compass rose - y
    radius = ww * 0.45   # Radius of compass rose
  
    # Compass rose
    pygame.draw.circle(self.imgbuf, self.black, (centx, centy), radius, 0)
    for i in range(0, 36*2):
      h = i / 2
      a = convert.degtorad(h * 10) - self.hdg
      inner_rad = 0.9 if ((h % 1) == 0) else 0.975
      x1 = centx + radius * inner_rad * math.sin(a)
      y1 = centy - radius * inner_rad * math.cos(a)
      x2 = centx + radius * 1.0 * math.sin(a)
      y2 = centy - radius * 1.0 * math.cos(a)
      xt = centx + radius * 0.8 * math.sin(a)
      yt = centy - radius * 0.8 * math.cos(a)
      pygame.draw.line(self.imgbuf, self.white, (x1, y1), (x2, y2), 3)
 
      col = self.white 
      if h == 0:
        t = 'N'
        col = self.yellow
      elif h == 9:
        t = 'E'
        col = self.yellow
      elif h == 18:
        t = 'S'
        col = self.yellow
      elif h == 27:
        t = 'W'
        col = self.yellow
      elif h % 3 == 0:
        t = f"{int(h):d}"
      else:
        t = ""
  
      if t != "":
        text = self.font24.render(t, True, col, self.black)
        rtext = pygame.transform.rotate(text, -convert.radtodeg(a))
        textRect = rtext.get_rect()
        textRect.center = (xt, yt)
        self.imgbuf.blit(rtext, textRect)
 
    pygame.draw.line(self.imgbuf, self.white, (centx, centy - radius * 0.5), (centx, centy - radius * 0.9), 3) 
    text = self.font32.render(f"{int(convert.radtodeg(self.hdg)):03d}",
                              True, self.yellow, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy - hh * 0.1)
    self.imgbuf.blit(text, textRect)
  
  # Draw pitch lines on artificial horizon
  # Params: surf - surface to draw on
  #         pl - pitch for pitch line in degrees
  #         l - length of pitch line
  #         withtext - if True, label the line
  def draw_pitchline(self, surf, pl, l, withtext):
    (sx, sy) = surf.get_size()
    radius = sx / 2
    max_pitch = 30.0 # Must agree with the horizon code
    pitch_px = (convert.radtodeg(self.pitch) + pl) * radius / max_pitch
    hcent = radius + pitch_px * self.sin_roll
    vcent = radius + pitch_px * self.cos_roll
    x1 = hcent - l/2 * self.cos_roll
    x2 = hcent + l/2 * self.cos_roll
    y1 = vcent + l/2 * self.sin_roll
    y2 = vcent - l/2 * self.sin_roll
    pygame.draw.line(surf, self.white, (x1, y1), (x2, y2), self.rescale_y(2))
    if (withtext and pl != 0):
      text = self.font24.render(f"{int(math.fabs(pl)):2d}",
                                True, self.white, self.blue if pl < 0 else self.brown)
      rtext = pygame.transform.rotate(text, convert.radtodeg(self.roll))
      textRect = rtext.get_rect()
      textRect.center = (x2, y2)
      surf.blit(rtext, textRect)

  # Airspeed indicator 
  def draw_asi(self, x, y, size):
    fullscale = 200.0
    stall     = 45.0
    vne       = 160.0
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/20, 0)
    for i in range (0, int(fullscale/10)+1):
      spd = (i*10)
      if spd <= stall:
        color = self.red
      elif spd >= vne:
        color = self.red
      else:
        color = self.green
      text = self.font16.render(f"{spd:d}", True, color, self.black)
      textRect = text.get_rect()
      ang = convert.degtorad(spd/fullscale * 270 - 240)
      x = centx + size*0.4*math.cos(ang)
      y = centy + size*0.4*math.sin(ang)
      textRect.center = (x, y)
      self.imgbuf.blit(text, textRect)
    text = self.font24.render("IAS Knots", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy-size/5)
    self.imgbuf.blit(text, textRect)

    ang = convert.degtorad((self.airspeed / fullscale) * 270 - 240)
    x = centx + size*0.4*math.cos(ang)
    y = centy + size*0.4*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent, (x, y), self.rescale_y(8))
   
  # Turn coordinator or "turn and slip" 
  def draw_turn_coord(self, x, y, size):   
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)

    r4  = self.rescale_y(4)
    r6  = self.rescale_y(6)
    r8  = self.rescale_y(8)
    r10 = self.rescale_y(10)
    r20 = self.rescale_y(20)

    # Sideslip bubble
    ssmax = 5.0
    ss = self.sideslip
    ss = ss if ss < ssmax else ssmax
    ss = ss if ss > -ssmax else -ssmax
    pygame.draw.rect(self.imgbuf, self.white,
                     (centx-size/3, centy+size/4-r10, size/1.5, r20), 1)
    pygame.draw.circle(self.imgbuf, self.white,
                       (centx + ss * size / 20, centy + size / 4), r10, 1)

    # Turn rate
    pygame.draw.circle(self.imgbuf, self.white, (centx, centy+size/7), size/30, 0)
    ang = self.turnrate * 10
    # Needle limits
    if (ang > math.pi / 3):
      ang = math.pi / 3
    if (ang < -math.pi / 3):
      ang = -math.pi / 3
    ang -= math.pi / 2
    x = centx + size * 0.3 * math.cos(ang)
    y = centy + size * 0.3 * math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, (centx, centy+size/7), (x, y), r10)

    # Dot for two-minute turn (3 deg/sec)
    ang = convert.degtorad(3.0) * 10 - math.pi / 2
    x = centx + size * 0.3 * math.cos(ang)
    y = centy + size * 0.3 * math.sin(ang)
    pygame.draw.circle(self.imgbuf, self.white, (x, y), r8)
    x = centx - size * 0.3 * math.cos(ang)
    pygame.draw.circle(self.imgbuf, self.white, (x, y), r8)

    # Dot for one-minute turn (6 deg/sec)
    ang = convert.degtorad(6.0) * 10 - math.pi / 2
    x = centx + size * 0.3 * math.cos(ang)
    y = centy + size * 0.3 * math.sin(ang)
    pygame.draw.circle(self.imgbuf, self.white, (x, y), r6)
    x = centx - size * 0.3 * math.cos(ang)
    pygame.draw.circle(self.imgbuf, self.white, (x, y), r6)
    
  # Artificial horizon 
  def draw_horizon(self, x, y, size):   
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)

    # offset allows the circular gauge to be smaller than the bounding square region
    offset = self.rescale_x(8)
    radius = size / 2 - offset
    # horimgbuf is of size radius*2 square. Will be cropped to a circle below.
    horimgbuf = pygame.Surface((radius*2, radius*2))

    # Draw brown/blue horizon
    # Artificial horizon
    l = radius * 2
    imsize_y_deg = 90       # In degrees of pitch
    max_pitch = 30.0        # Range of horizon +/- degrees
    pitch_deg = convert.radtodeg(self.pitch)
    pitch_px = pitch_deg * radius / max_pitch
    hcent = radius + pitch_px * self.sin_roll
    vcent = radius + pitch_px * self.cos_roll
    x1 = hcent - l * self.cos_roll
    x2 = hcent + l * self.cos_roll
    y1 = vcent + l * self.sin_roll
    y2 = vcent - l * self.sin_roll
    pitch_px = (pitch_deg - imsize_y_deg) * radius / max_pitch
    hcent = radius + pitch_px * self.sin_roll
    vcent = radius + pitch_px * self.cos_roll
    x3 = hcent - l * self.cos_roll
    x4 = hcent + l * self.cos_roll
    y3 = vcent + l * self.sin_roll
    y4 = vcent - l * self.sin_roll
    pygame.draw.polygon(horimgbuf, self.blue, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])
    pitch_px = (pitch_deg + imsize_y_deg) * radius / max_pitch
    hcent = radius + pitch_px * self.sin_roll
    vcent = radius + pitch_px * self.cos_roll
    x3 = hcent - l * self.cos_roll
    x4 = hcent + l * self.cos_roll
    y3 = vcent + l * self.sin_roll
    y4 = vcent - l * self.sin_roll
    pygame.draw.polygon(horimgbuf, self.brown, [(x1, y1), (x2, y2), (x4, y4), (x3, y3)])

    r6 = self.rescale_y(6)
    r8 = self.rescale_y(8)
    r20 = self.rescale_y(20)
    r50 = self.rescale_y(50)
    r75 = self.rescale_y(75)
    r100 = self.rescale_y(100)
    r200 = self.rescale_y(200)
    r300 = self.rescale_y(300)

    # Airplane symbol 
    pygame.draw.line(horimgbuf, self.yellow, (r200, radius), (r300, radius), r8)
    pygame.draw.line(horimgbuf, self.yellow, (2*radius-r300, radius), (2*radius-r200, radius), r8)
    pygame.draw.line(horimgbuf, self.yellow, (radius-r50, radius+r20), (radius, radius), r6)
    pygame.draw.line(horimgbuf, self.yellow, (radius+r50, radius+r20), (radius, radius), r6)

    # Pitch graticule
    for pl in range(-8, 8):
      self.draw_pitchline(horimgbuf, pl * 10,       r100, True)
      self.draw_pitchline(horimgbuf, pl * 10 + 2.5, r50,  False)
      self.draw_pitchline(horimgbuf, pl * 10 + 5,   r75,  False)
      self.draw_pitchline(horimgbuf, pl * 10 + 7.5, r50,  False)
   
    # Use alpha channel to extract circular portion of horimgbuf
    horimgbuf.convert_alpha()
    maskimg = pygame.Surface(horimgbuf.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(maskimg, (128,128,128,255), (0, 0, radius*2, radius*2), 0)
    pygame.draw.ellipse(maskimg, (255, 255, 255, 0), horimgbuf.get_rect())
    horimgbuf.blit(maskimg, (0, 0), special_flags=0) # pygame.BLEND_RGBA_MIN)
    self.imgbuf.blit(horimgbuf, (x+offset, y+offset), (0, 0, radius*2, radius*2))

    # Ring around the instrument
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)

    for a in [-45, -30, 0, +30, +45]:
      ang = convert.degtorad(a - 90)
      x = centx + size*0.45*math.cos(ang)
      y = centy + size*0.45*math.sin(ang)
      pygame.draw.circle(self.imgbuf, self.white, (x, y), self.rescale_y(6))
    
  # Gyro compass 
  def draw_compass(self, x, y, size):   
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    self.draw_rose(x, y, (size, size))
    
  # Altimeter 
  def draw_alt(self, x, y, size):   
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/20, 0)
    for i in range (0, 10):
      text = self.font32.render(f"{i:d}", True, self.white, self.black)
      textRect = text.get_rect()
      ang = convert.degtorad(i * 36 - 90)
      x = centx + size*0.4*math.cos(ang)
      y = centy + size*0.4*math.sin(ang)
      textRect.center = (x, y)
      self.imgbuf.blit(text, textRect)
    text = self.font24.render("ALT ftx1000", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy-size/5)
    self.imgbuf.blit(text, textRect)

    ang = convert.degtorad(self.altitude / 100000.0 * 360 - 90) # Outer
    x = centx + size*0.45*math.cos(ang)
    y = centy + size*0.45*math.sin(ang)
    pygame.draw.circle(self.imgbuf, self.white, (x, y), self.rescale_y(8))
    ang = convert.degtorad(self.altitude / 10000.0 * 360 - 90) # Hour hand
    x = centx + size*0.25*math.cos(ang)
    y = centy + size*0.25*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent, (x, y), self.rescale_y(14))
    ang = convert.degtorad(self.altitude / 1000.0 * 360 - 90) # Minute hand
    x = centx + size*0.4*math.cos(ang)
    y = centy + size*0.4*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent, (x, y), self.rescale_y(4))
    
  # Vertical Speed Indicator (or "Rate of Climb") 
  def draw_vsi(self, x, y, size):   
    fullscale = 5000
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/20, 0)
    for i in range (-int(fullscale/1000), int(fullscale/1000)+1):
      roc = i * 1000
      text = self.font32.render(f"{i:+d}", True, self.white, self.black)
      textRect = text.get_rect()
      ang = convert.degtorad(roc/fullscale * 130 - 180)
      x = centx + size*0.4*math.cos(ang)
      y = centy + size*0.4*math.sin(ang)
      textRect.center = (x, y)
      self.imgbuf.blit(text, textRect)
    text = self.font24.render("FPM x1000", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy-size/5)
    self.imgbuf.blit(text, textRect)

    ang = (self.roc / fullscale) * 130
    # End stops for pointer
    if ang > 150:
      ang = 150
    if ang < -150:
      ang = -150
    ang = convert.degtorad(ang - 180)
    x = centx + size*0.35*math.cos(ang)
    y = centy + size*0.35*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent, (x, y), self.rescale_y(16))

  # Draw RPM guage
  def draw_rpm(self, x, y, size):
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/20, 0)
    for i in range (0, 8):
      rpm = i * 5
      text = self.font24.render(f"{rpm:d}", True, self.white, self.black)
      textRect = text.get_rect()
      ang = (rpm / 40) * 270
      ang = convert.degtorad(ang - 225)
      x = centx + size*0.4*math.cos(ang)
      y = centy + size*0.4*math.sin(ang)
      textRect.center = (x, y)
      self.imgbuf.blit(text, textRect)
    text = self.font24.render("RPM x100", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy-size/5)
    self.imgbuf.blit(text, textRect)

    ang = (self.rpm / 4000) * 270
    ang = convert.degtorad(ang - 225)
    x = centx + size*0.4*math.cos(ang)
    y = centy + size*0.4*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent, (x, y), self.rescale_y(8))
   
  # Draw fuel-flow and EGT dual guage
  def draw_ff_egt(self, x, y, size):
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    cent_l = (centx - size/15, centy)
    cent_r = (centx + size/15, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent_l, size/20, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent_r, size/20, 0)

    text = self.font16.render("90", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/5, centy-size/3)
    self.imgbuf.blit(text, textRect)
    text = self.font16.render("0", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/5, centy+size/3)
    self.imgbuf.blit(text, textRect)
    text = self.font16.render("FLOW", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/3, centy)
    self.imgbuf.blit(text, textRect)
    text = self.font16.render("lbs/hr", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/3, centy+size/10)
    self.imgbuf.blit(text, textRect)

    text = self.font16.render("EGT", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx+size/3, centy)
    self.imgbuf.blit(text, textRect)

    if self.fuel_flow > 90:
      self.fuel_flow = 90
    if self.fuel_flow < 0:
      self.fuel_flow = 0
    ang = (self.fuel_flow / 90) * 140
    ang = convert.degtorad(ang - 250)
    x = (centx - size/15) + size*0.3*math.cos(ang)
    y = centy + size*0.3*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent_l, (x, y), self.rescale_y(4))
  
    if self.egt > 1300:
      self.egt = 1300
    if self.egt < 900:
      self.egt = 900
    ang = ((900 - self.egt) / 400) * 140
    ang = convert.degtorad(ang + 70)
    x = (centx + size/15) + size*0.3*math.cos(ang)
    y = centy + size*0.3*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent_r, (x, y), self.rescale_y(4))
  
  # Draw dual fuel gauge
  def draw_fuel(self, x, y, size):
    centx = x + size / 2
    centy = y + size / 2
    cent = (centx, centy)
    cent_l = (centx - size/15, centy)
    cent_r = (centx + size/15, centy)
    pygame.draw.circle(self.imgbuf, self.black, cent, size/2, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent, size/2, 2)
    pygame.draw.circle(self.imgbuf, self.white, cent_l, size/20, 0)
    pygame.draw.circle(self.imgbuf, self.white, cent_r, size/20, 0)

    text = self.font16.render("28", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/5, centy-size/3)
    self.imgbuf.blit(text, textRect)
    textRect.center = (centx+size/5, centy-size/3)
    self.imgbuf.blit(text, textRect)
    text = self.font16.render("0", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx-size/5, centy+size/3)
    self.imgbuf.blit(text, textRect)
    textRect.center = (centx+size/5, centy+size/3)
    self.imgbuf.blit(text, textRect)
    text = self.font16.render("FUEL gal", True, self.white, self.black)
    textRect = text.get_rect()
    textRect.center = (centx, centy-size/5)
    self.imgbuf.blit(text, textRect)

    ang = (self.fuel_left / 106) * 140
    ang = convert.degtorad(ang - 250)
    x = (centx - size/15) + size*0.3*math.cos(ang)
    y = centy + size*0.3*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent_l, (x, y), self.rescale_y(4))
  
    ang = (self.fuel_right / 106) * 140
    ang = convert.degtorad(70 - ang)
    x = (centx + size/15) + size*0.3*math.cos(ang)
    y = centy + size*0.3*math.sin(ang)
    pygame.draw.line(self.imgbuf, self.white, cent_r, (x, y), self.rescale_y(4))
   
   
  # Draw control positions
  def draw_controls(self, x, y, size):
    r15 = self.rescale_y(15)
    r20 = self.rescale_y(20)
    r30 = self.rescale_y(30)
    pygame.draw.rect(self.imgbuf, self.black, (x, y, r30, size), 1)
    pygame.draw.circle(self.imgbuf, self.black, (x+r15, y + size - size * self.throttle), r30)
    pygame.draw.rect(self.imgbuf, self.black, (x + size/4, y, r30, size), 1)
    pygame.draw.circle(self.imgbuf, self.red, (x+r15 + size/4, y + size - size * self.mixture), r30)
    x += size / 2
    pygame.draw.rect(self.imgbuf, self.black, (x, y, size, size), 0)
    border = self.rescale_y(10)
    size -= border*2
    x += border
    y += border
    pygame.draw.rect(self.imgbuf, self.red, (x, y, size, size), 1)
    pygame.draw.circle(self.imgbuf, self.red,
                       (x+size/2+size/2*self.aileron, y+size/2+size*self.elevator), r20)
    pygame.draw.circle(self.imgbuf, self.red,
                       (x+size/2+size/2*self.rudder, y+size), r20,
                       1 if self.autorudder == True else 0)
    if self.flap > 0:
      text = self.font32.render(f"FLAPS {int(self.flap*10):d}", True, self.red, self.black)
      textRect = text.get_rect()
      textRect.center = (x + size*0.8, y + size * 0.05)
      self.imgbuf.blit(text, textRect)
    

  # Draw Steam Panel.  Main entry point.
  def draw(self, roll, pitch, hdg, yaw_d, x_d, z_world, z_d_world,
           aileron, elevator, rudder, throttle, mixture, flap, autorudder, y_dd, alpha,
           rpm, fuel_flow, egt, fuel_left, fuel_right):
    (w, h) = self.size

    self.roll      = roll
    self.pitch     = pitch
    self.hdg       = hdg
    self.turnrate  = yaw_d
    self.sideslip  = y_dd
    self.airspeed  = convert.speedtoknots(x_d)
    self.roc       = convert.speedtofeetpermin(z_d_world)
    self.altitude  = convert.metrestofeet(z_world)
    self.rpm       = rpm
    self.fuel_flow = fuel_flow
    self.egt       = egt
    self.fuel_left = fuel_left
    self.fuel_right= fuel_right

    self.aileron    = aileron
    self.elevator   = elevator
    self.rudder     = rudder
    self.throttle   = throttle
    self.mixture    = mixture
    self.flap       = flap
    self.autorudder = autorudder

    self.sin_roll = math.sin(roll)
    self.cos_roll = math.cos(roll)

    pygame.draw.rect(self.imgbuf, self.grey, (0, 0, w, h), 0)
    border = 10
    diameter = h/2.1
    spacing = h/2.0
    self.draw_ff_egt(border+spacing/4, border+spacing/4, diameter*0.75)
    self.draw_fuel(border+spacing/4, border+spacing, diameter*0.75)
    self.draw_asi(border+spacing, border, diameter)
    self.draw_turn_coord(border+spacing, border+spacing, diameter)
    self.draw_horizon(border+2*spacing, border, diameter)
    self.draw_compass(border+2*spacing, border+spacing, diameter)
    self.draw_alt(border+3*spacing, border, diameter)
    self.draw_vsi(border+3*spacing, border+spacing, diameter)
    self.draw_rpm(border+4*spacing, border+spacing, diameter*0.75)
    self.draw_controls(border+4.8*spacing, border+diameter/4, diameter*1.5)

    # Angle of attack
    text = self.font24.render(f"\u03b1={convert.radtodeg(alpha):+0.1f}\u00b0", True, self.magenta, self.black)
    textRect = text.get_rect()
    textRect.center = (10, 10)
    self.imgbuf.blit(text, textRect)
    
    (sx, sy) = self.size 
    self.display.blit(self.imgbuf, self.offset, (0, 0, sx, sy)) # Blit buffer to real display
    pygame.display.flip()
  
  
