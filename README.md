# PyFlightSim
Simple flight simulator written in Python 3 / Pygame.

![Ready for takeoff!](https://github.com/bobbimanners/PyFlightSim/blob/main/screenshot.png?raw=true)

# What is PyFlightSim

# Prerequisites

# Key Mapping

## Control Surfaces

The keys for the control surfaces (elevator, ailerons, rudder, flaps and trim) are the same as those from the venerable Sublogic Flight Simulator 2 for the Apple II.  It is based on these adjacent keys:
```
   R  T  Y
   F  G  H
C  V  B  N M
```
The 'stick' is controlled by:
```
      T
   F  G  H
      B
```
So `T` is elevator down while `B` is elevator up.  `F` and `H` move the ailerons to bank left and right, and `G` centres the ailerons.

To the right of this cluster, `Y` is flaps up one notch and `N` is flaps down one notch.

To the left, `R` is trim forward and `V` is trim back (trim is not currently implemented however.)

Finally `C` and `M` are rudder left and right respectively.

## Engine Controls

The throttle is controlled by the `-` and `=` keys on the main keypad.

The mixture is adjusted using the `[` and `]` keys immediately below.

`S` will fire the starter motor and attempt to start the engine.

## Brakes

`P` toggles the parking brake.  Holding down `SPACE` will engage the wheel brakes.

## Other

`Z` toggles the "auto-rudder" function.  This is on by default when airborne.  The auto-rudder feature will apply as much rudder as necessary to maintain a balanced turn.  You can disable it in order to perform sideslips and other aerobatic manoevers (such as aileron rolls.)

Autorudder turns off when on the ground, so you can steer using the rudder (`C` and `M`).

## View Controls

You can look all around you using the numeric keypad:
```
7 8 9
4   6
1 2 3
```
The `8` key will return you to the normal forwards looking view.

# Quick Take-off

- Press `S` to fire the starter.  Idle is around 600RPM.
- Disengage the parking brake with `P`.
- Advance the throttle to max by holding down `=` until the throttle is at the top (red circle).
- Plane will begin rolling forwards.
- Once you have around 60kts, smoothly pull back on the stick by hitting `B` a few times.  The nose should rise and the aircraft will be begin to climb.
- Establish an approximate 65kt climb (around 7 degrees nose up, 2700 RPM).
- Enjoy!

