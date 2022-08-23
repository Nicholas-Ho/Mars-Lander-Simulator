// Mars lander simulator
// Version 1.11
// Mechanical simulation functions
// Gabor Csanyi and Andrew Gee, August 2019

// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation, to make use of it
// for non-commercial purposes, provided that (a) its original authorship
// is acknowledged and (b) no modified versions of the source code are
// published. Restriction (b) is designed to protect the integrity of the
// exercise for future generations of students. The authors would be happy
// to receive any suggested modifications by private correspondence to
// ahg@eng.cam.ac.uk and gc121@eng.cam.ac.uk.

#include "lander.h"

// Global variable for Verlet integration
bool verlet_initialised = false;

void autopilot (void)
  // Autopilot to adjust the engine throttle, parachute and attitude control
{
  // INSERT YOUR CODE HERE
}

vector3d calculate_acceleration () {
  // Calculate total mass (lander + fuel)
  double mass;
  mass = UNLOADED_LANDER_MASS + (FUEL_CAPACITY * FUEL_DENSITY * fuel);

  // Calculate Acceleration via Forces
  vector3d thr, gravity, lander_drag, chute_drag, acceleration;

  thr = thrust_wrt_world();
  gravity = -(GRAVITY * MARS_MASS * mass) * position.norm() / position.abs2();
  lander_drag = -0.5 * atmospheric_density(position) * DRAG_COEF_LANDER * (M_PI*LANDER_SIZE*LANDER_SIZE) * velocity.abs2() * velocity.norm();
  
  if (parachute_status == DEPLOYED) {
    chute_drag = -0.5 * atmospheric_density(position) * DRAG_COEF_LANDER * (5.0*2.0*LANDER_SIZE*2.0*LANDER_SIZE) * velocity.abs2() * velocity.norm();
  } else {
    chute_drag = vector3d(0, 0, 0);
  }

  acceleration = (thr + gravity + lander_drag + chute_drag) / mass;

  return acceleration;
}

void euler_update () {

  // Acceleration
  vector3d acceleration = calculate_acceleration();

  // Position
  position = position + (delta_t*velocity);

  // Velocity
  velocity = velocity + (delta_t*acceleration);
}

void verlet_update () {

  // Static variable that stores the position two cycles ago
  static vector3d next_position;
  vector3d prev_position; // To be updated with current position each cycle

  // If this is the first cycle (verlet_initialised = false), use Euler to determine next_position
  // Otherwise, use Verlet
  if (verlet_initialised) {

    // Step through to the current step
    prev_position = position;
    position = next_position;

    // Calculate current acceleration
    vector3d acceleration = calculate_acceleration();

    // Calculate next position
    next_position = (2 * position) - prev_position + (delta_t * delta_t * acceleration);

    // Calculate current velocity
    velocity = (next_position - prev_position) / (2 * delta_t);

  } else {
    next_position = position + (delta_t*velocity);
    verlet_initialised = true;
    verlet_update();
  }

}

void numerical_dynamics (void)
  // This is the function that performs the numerical integration to update the
  // lander's pose. The time step is delta_t (global variable).
{
  verlet_update();

  // Here we can apply an autopilot to adjust the thrust, parachute and attitude
  if (autopilot_enabled) autopilot();

  // Here we can apply 3-axis stabilization to ensure the base is always pointing downwards
  if (stabilized_attitude) attitude_stabilization();
}

void initialize_simulation (void)
  // Lander pose initialization - selects one of 10 possible scenarios
{
  // The parameters to set are:
  // position - in Cartesian planetary coordinate system (m)
  // velocity - in Cartesian planetary coordinate system (m/s)
  // orientation - in lander coordinate system (xyz Euler angles, degrees)
  // delta_t - the simulation time step
  // boolean state variables - parachute_status, stabilized_attitude, autopilot_enabled
  // scenario_description - a descriptive string for the help screen

  scenario_description[0] = "circular orbit";
  scenario_description[1] = "descent from 10km";
  scenario_description[2] = "elliptical orbit, thrust changes orbital plane";
  scenario_description[3] = "polar launch at escape velocity (but drag prevents escape)";
  scenario_description[4] = "elliptical orbit that clips the atmosphere and decays";
  scenario_description[5] = "descent from 200km";
  scenario_description[6] = "";
  scenario_description[7] = "";
  scenario_description[8] = "";
  scenario_description[9] = "";

  switch (scenario) {

  case 0:
    // a circular equatorial orbit
    position = vector3d(1.2*MARS_RADIUS, 0.0, 0.0);
    velocity = vector3d(0.0, -3247.087385863725, 0.0);
    orientation = vector3d(0.0, 90.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    break;

  case 1:
    // a descent from rest at 10km altitude
    position = vector3d(0.0, -(MARS_RADIUS + 10000.0), 0.0);
    velocity = vector3d(0.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = true;
    autopilot_enabled = false;
    break;

  case 2:
    // an elliptical polar orbit
    position = vector3d(0.0, 0.0, 1.2*MARS_RADIUS);
    velocity = vector3d(3500.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    break;

  case 3:
    // polar surface launch at escape velocity (but drag prevents escape)
    position = vector3d(0.0, 0.0, MARS_RADIUS + LANDER_SIZE/2.0);
    velocity = vector3d(0.0, 0.0, 5027.0);
    orientation = vector3d(0.0, 0.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    break;

  case 4:
    // an elliptical orbit that clips the atmosphere each time round, losing energy
    position = vector3d(0.0, 0.0, MARS_RADIUS + 100000.0);
    velocity = vector3d(4000.0, 0.0, 0.0);
    orientation = vector3d(0.0, 90.0, 0.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = false;
    autopilot_enabled = false;
    break;

  case 5:
    // a descent from rest at the edge of the exosphere
    position = vector3d(0.0, -(MARS_RADIUS + EXOSPHERE), 0.0);
    velocity = vector3d(0.0, 0.0, 0.0);
    orientation = vector3d(0.0, 0.0, 90.0);
    delta_t = 0.1;
    parachute_status = NOT_DEPLOYED;
    stabilized_attitude = true;
    autopilot_enabled = false;
    break;

  case 6:
    break;

  case 7:
    break;

  case 8:
    break;

  case 9:
    break;

  }

  // Reset the Verlet integration static variable
  verlet_initialised = false;
}
