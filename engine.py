#!/usr/bin/python3

import propeller
import convert
import math

# Naturally-aspirated piston engine model
# Extremely simple model:
#  - Torque curve is flat, max_torque available at all RPMs
#  - Power curve is linear with RPM (consequence of above)
# The reality is more complex, but this is good enough for our purposes
class PistonEngine:
  prop         = propeller.FixedPitchProp() # Propeller model
  moi          = 1.5     # Typical MOI for small prop

  delta_t      = 0.1     # Simulation interval
  rho_0        = 1.225   # Density of air in kg/m^3 at sea level
  max_power_sl = 120.0e3 # Power at sea-level (Cessna 172 120kW Lycoming IO-360-L2A)
  max_rpm      = 2700    # Max rated RPM
  min_rpm      = 550     # Min RPM engine can idle at
  idle_rpm     = 600     # Idle RPM
  full_rich    = 10      # Full rich air to fuel at sea level
  full_lean    = 20      # Full lean air to fuel at sea level
  mix_max_p    = 12.5    # Mixture for max power cruise
  mix_best_ec  = 16.0    # Mixture for best economy cruise
  mix_peak_egt = 15.0    # Mixture where EGT peaks
  rpm          = 0       # Revs per minute
  egt          = 0       # Exhaust gas temp, fahrenheit
  fuel_flow    = 0       # Fuel flow, in lbs/hr
  running      = False

  # Params: delta_t is the simulation interval in seconds
  def __init__(self, delta_t):
    self.delta_t = delta_t

  # Params: tas      - true airspeed m/s
  #         throttle - throttle setting (0 to 1)
  #         mixture  - mixture setting (0 to 1)
  #         starter  - True if starter is activated
  #         rho      - air density
  #         altitude - altitude in m
  #         fuellev  - amount of fuel remaining
  # Returns (rpm, thrust, fuel_flow, egt)
  def update(self, tas, throttle, mixture, starter, rho, altitude, fuellev):
 
    if starter == True:
      print("Attempting to start ...")
      self.rpm = 1000
      self.running = True

    # Throttle calibration
    idle_throt = 0.1
    throttle = idle_throt + throttle * (1 - idle_throt)

    # Work out the air to fuel ratio
    af_ratio = (self.full_lean + (self.full_rich - self.full_lean) * mixture) * (rho / self.rho_0)
    #print("A:F Ratio: ", af_ratio, rho)

    if mixture < 0.05 or fuellev < 0 or self.rpm < self.min_rpm:
      self.running = False # Fuel cut-off
    
    # 3% loss of power per 1000ft
    max_power = self.max_power_sl * (1.0 - 0.03 * altitude / 304.8)

    # Effect of mixture on power
    # Based on Fig 3-1 from Lycoming O-360 Operator's Manual, linearized
    if af_ratio > self.mix_best_ec:
      pct = 92.5 - (af_ratio - self.mix_best_ec) * 10
    elif af_ratio > self.mix_max_p:
      pct = 92.5 + (af_ratio - self.mix_best_ec)/(self.mix_max_p - self.mix_best_ec) * 7.5 # 100% at mix_max_p
    else:
      pct = 100.0 - (self.mix_max_p - af_ratio) * 2
    print("Percent of max power is ", pct)
    max_power *= pct / 100.0

    max_torque = max_power / convert.rpmtoradpersecond(self.max_rpm)
    engine_torque = max_torque * throttle if self.running == True else 0.0

    (prop_thrust, prop_torque, shaft_power) = self.prop.update(self.rpm, tas, rho)

    # Friction within the engine
    # Set up empirically to get reasonable behaviour for spin-down when the power
    # is cut and maximum RPM at full throttle
    frict_a = 20
    frict_b = 0.0
    frict_c = 2.0e-5
    frict_torque = frict_a + frict_b * self.rpm + frict_c * self.rpm * self.rpm

    print(f"Engine {engine_torque:.2f} Prop {prop_torque:.2f} Frict {frict_torque:.2f}")
    ang_acc = (engine_torque - prop_torque - frict_torque) / self.moi
    self.rpm += convert.radpersecondtorpm(ang_acc) * self.delta_t

    if self.rpm < 0:
      self.rpm = 0

    # Exhaust gas temperature - from Fig 3-1 from Lycoming O-360 Operator's Manual
    if self.running == True:
      if af_ratio > self.mix_peak_egt:
        delta_egt = (af_ratio - self.mix_peak_egt) * -10
      else:
        delta_egt = (af_ratio - self.mix_peak_egt) * 20
      tgt_egt = 1200 + delta_egt # 1200F is a reasonable mean EGT
    else:
      tgt_egt = 0
    a = 0.01 # Exponential average
    self.egt = a * tgt_egt + (1 - a) * self.egt

    # Fuel flow - this is a complete guess. Engines are complicated.
    tgt_fuel_flow = 9/14 * 1e-3 * self.rpm * engine_torque / af_ratio # Tweaked so max is 90 lbs/hr
    a = 0.05 # Exponential average
    self.fuel_flow = a * tgt_fuel_flow + (1 - a) * self.fuel_flow

    return (self.rpm, prop_thrust, self.fuel_flow, self.egt)

