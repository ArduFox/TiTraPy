# coding: utf-8
# https://github.com/jsbain/uicomponents/blob/master/colorpicker.py

# https://github.com/khilnani/pythonista-scripts/blob/master/thirdparty/UI/jsbin-uicomponents/colorpicker.py
import ui, colorsys, math

# how can i return a value?
# if passed as parameter can i change its value? probably yes if its for example a list
#
# does a view have return value?
# nothing to find in the documentation
#
#
# changed:
#
# v has a non linear slope and an offset to be sure 1.0 is reached


class ColorPicker(ui.View):
  def __init__(self, color, *args, **kwargs):
    # TODO add parameter to set startvalue of color
    ui.View.__init__(self, *args, **kwargs)
    self.history = []  #future...keep track of recent colors
    
    r,g,b,a=ui.parse_color(color)
    h,s,v=colorsys.rgb_to_hsv(r,g,b)
    self.current = (h,s,v)    
#    self.current = (.3, 0.2, 0.9)
    self.N = 12    # grid for hue and saturation
    self.Nb = 18   # grid for value
    self.__debugprint=True

  def draw(self):
    square_size = min(self.width, self.height)
    N = self.N
    Nb = self.Nb
    dx = square_size * 1.0 / (N + 2)
    dxb = N * dx / Nb
    h, s, v = self.current
    i0, j0, k0 = (round(c * N) for c in self.current)
    
    offset = 1.0 - (math.sqrt(Nb-1) *  1. / math.sqrt(Nb))

    # k0 holds the number of field in value slider
    # at drawing in line 45 k and Nb are scaled by square root
    #
    # v = (math.sqrt(k) *  1. / math.sqrt(Nb)
    # v * math.sqrt(NB) = math.sqrt(k)
    # v * v * NB = k
    
    scv=self.current[2]-offset # remove when debugging is done
    k0 = round(scv * scv * Nb )
    #print (f" sel     {float(scv):.3} * Nb = {float(scv * Nb):3.3} ^2*Nb= {float(scv * scv * Nb):3.3} k0 = {k0}")
    # poking around - should do my math
    #    k0 = 
    #draw H/S grid
    for i in range(0, N):
      for j in range(0, N):
        ui.set_color(colorsys.hsv_to_rgb(i * 1.0 / N, j * 1.0 / N, v))
        ui.set_blend_mode(ui.BLEND_NORMAL)
        ui.fill_rect(round(i * dx), round(j * dx), round(dx), round(dx))

    #draw V slider
    for k in range(0, Nb):
      ui.set_color(colorsys.hsv_to_rgb(h, s, offset+(math.sqrt(k) *  1. / math.sqrt(Nb))))
      #if self.__debugprint :
        #print (f"draw {k} = {(math.sqrt(k) *  1. / math.sqrt(Nb)):.3} off {offset:.3}") 
      # 1-(..) would look nicer but is lot of rework in code
      # v=1.0 should always be in reach -> how can this be certain?
      # dont need the darker shades, but more od the lighter ones
      # add offset?
      # steeper curve? quadratic would maybe be to steep
      ui.set_blend_mode(ui.BLEND_NORMAL)
      ui.fill_rect(
        round((N + 1) * dx), round(k * dxb), round(dx), round(dxb + 0.5))

    #self.__debugprint=False
    #highlight selection
    if all([c >= 0 for c in self.current]):
      #				ui.set_color(colorsys.hsv_to_rgb(h,s,1-0.5*(1-v)))
      ui.set_color(
        colorsys.hsv_to_rgb(1 - 0.5 * (1 - h), (1 - s), 1 - 0.5 * (1 - v)))
      p = ui.Path.rect(i0 * dx, j0 * dx, dx, dx)
      p.line_width = 4
      p.stroke()

      ui.set_color(colorsys.hsv_to_rgb(1 - 0.5 * (1 - h), (1-s), 1 - 0.5 * (1 - v)))
      p = ui.Path.rect((N + 1) * dx, k0 * dxb, dx, dxb)
      p.line_width = 4
      p.stroke()
      #preview
      ui.set_color(colorsys.hsv_to_rgb(h, s, v))
      ui.fill_rect(0, (N + 1) * dx, 6 * dx, dx)
      r, g, b = colorsys.hsv_to_rgb(h, s, v)

      clip = lambda x: min(max(x, 0), 1)
      rp, gp, bp = colorsys.hsv_to_rgb(1 - h, 1, clip((0.5 - v) * 100))
      ui.draw_string(
        ('{:02x}' * 3).format(int(r * 255), int(g * 255), int(b * 255)),
        (0, (N + 1) * dx, 6 * dx, dx),
        alignment=ui.ALIGN_CENTER,
        color=(rp, gp, bp))

  def touch_began(self, touch):
    self.touch_moved(touch)

  def touch_moved(self, touch):
    #set color
    #  self dx=size/(N+2)
    square_size = min(self.width, self.height)
    N = self.N
    Nb = self.Nb
    dx = square_size * 1.0 / (N + 2)
    dxb = N * dx * 1.0 / Nb
    h, s, v = self.current
    offset = 1.0 - (math.sqrt(Nb-1) *  1. / math.sqrt(Nb))
    if touch.location[0] >= dx * (N + 1) and touch.location[1] <= dxb * Nb:
      v = math.sqrt(max(round(touch.location[1]/ dxb - 0.1),0)) / math.sqrt(float(Nb))+offset  
      print (f"\n touch v={v:3.3}    dxb={dxb:3.3}              k = {round(touch.location[1]/dxb)}")
    elif touch.location[1] <= dx * N and touch.location[0] <= dx * N:
      h = round(touch.location[0] / dx - 0.5) / N
      s = round(touch.location[1] / dx - 0.5) / N
    clip = lambda x: min(max(x, 0), 1)
    self.current = (clip(h), clip(s), clip(v))
    self.set_needs_display()

  def GetColor(self):
    r, g, b = colorsys.hsv_to_rgb(self.current[0],self.current[1],self.current[2])
    return ('{:02x}' * 3).format(int(r * 255), int(g * 255), int(b * 255))


#v=ColorPicker(frame=(0,0,360,576))
v = ColorPicker("darkorange",frame=(0, 0, 360, 360))
v.present('sheet')
print(v.GetColor())
v.wait_modal()
print(v.GetColor())
