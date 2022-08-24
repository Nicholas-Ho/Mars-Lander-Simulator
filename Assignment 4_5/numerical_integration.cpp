
#include "lander.h"

// Global variable for Verlet integration
bool verlet_initialised = false;

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

void reset_integration_state () {
  verlet_initialised = false;
}