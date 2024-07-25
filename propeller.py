#!/usr/bin/python3

import math
import convert

# Fixed-pitch propeller model
# Calculations use Actuator Disk Theory and are then corrected empirically using
# measured coefficients of thrust and torque.  For equations see:
# https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node86.html
class FixedPitchProp:
  # Specs are for McCauley propeller (Cessna 172A through H, with O-300)
  diameter        = 1.94       # Rotor diameter in metres
  peak_efficiency = 0.85       # About the best one can for for GA propeller

  # Return coeffients of thrust and coeffient of torque
  # Params: advance_ratio - advance ratio of propeller
  # Returns (coeff_thrust, coeff_torque, shaft_power)
  def calc_coefficients(self, advance_ratio):
    # Approximate linearization of the curves from this paper:
    # https://www.researchgate.net/figure/Propeller-model-thrust-coefficient-C-t-power-coefficient-C-p-and-propulsive_fig4_361496616

    if advance_ratio < 0.0:
      advance_ratio = 0.0
    elif advance_ratio > 0.6:
      advance_ratio = 0.6

    # Coefficient of thrust curve is approximately a straight line with
    # negative gradient. We add a slight convexity to the function to give
    # the efficiency curve the expected skew.
    coeff_thrust = 0.1 * (1.0 - advance_ratio / 0.6)
    convexity = 0.016667
    if advance_ratio < 0.3:
      coeff_thrust += advance_ratio * convexity
    else:
      coeff_thrust += (0.6 - advance_ratio) * convexity

    # The torque curve is approximated with a horizontal segment up to
    # advance_ratio 0.2, followed by a negative linear gradient.
    if advance_ratio < 0.2:
      coeff_torque = 0.03
    else:
      coeff_torque = (1.0 - (1.0 / 0.6) * (advance_ratio - 0.2)) * 0.03

    # The values in the researchgate.net paper above give a nice shape efficiency
    # curve but peak efficiency is around 0.1167. Should be around 0.85.
    # Based on this:
    # https://www.researchgate.net/figure/Propeller-Coefficient-of-Thrust-Torque-and-Efficiency_fig4_285581158
    # we can see that coeff_torque is too high. We reduce it to get 85% peak efficiency.
    coeff_torque /= (self.peak_efficiency / 0.1167)

    return(coeff_thrust, coeff_torque)

  # Return propeller thrust and torque.
  # Params: rpm is propeller RPM, tas is true airspeed in m/s, rho is air density
  # Returns (thrust, torque, shaft_power)
  def update(self, rpm, tas, rho):

    # Actuator Disk Theory Equations from here:
    # https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node86.html
    rot_rev_per_sec = rpm / 60.0
    if rot_rev_per_sec > 1e-3:
      advance_ratio = tas / (self.diameter * rot_rev_per_sec)
    else:
      advance_ratio = 1.0
    (thrust_coeff, torque_coeff) = self.calc_coefficients(advance_ratio)
    thrust = thrust_coeff * rho * rot_rev_per_sec ** 2 * self.diameter ** 4
    torque = torque_coeff * rho * rot_rev_per_sec ** 2 * self.diameter ** 5
    shaft_power = torque * rot_rev_per_sec * 2 * math.pi
    efficiency = (thrust_coeff * advance_ratio) / (2 * math.pi * torque_coeff)

    print(f"Advance ratio: {advance_ratio:.2f}")
    print(f"Prop Thrust:   {thrust:.1f} N")
    print(f"Prop Torque:   {torque:.1f} Nm")
    print(f"Shaft Power:   {shaft_power/1000:.0f} kW")
    print(f"Prop Eff:      {efficiency*100.0:.1f}%")
    return (thrust, torque, shaft_power)

