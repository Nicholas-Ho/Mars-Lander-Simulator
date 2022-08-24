// Abstracting out autopilot code

#include "lander.h"

// Forward-declare calculate_acceleration() from numerical_integration.cpp
vector3d calculate_acceleration();

// Constants
double height_const = 2e-2;
double controller_gain = 1.2;
double delta_offset = 0.5;

// Calculate error
double calculate_error () {
    double height = position.abs() - MARS_RADIUS;
    vector3d pos_norm = position.norm(); // Position unit vector
    return -(0.5 + height_const*height + velocity*pos_norm); // Scalar product of velocity and position unit vector
}

void autopilot (void)
  // Autopilot to adjust the engine throttle, parachute and attitude control
{
    // Calculate (pure) controller output
    double error, P_out;
    error = calculate_error();
    P_out = controller_gain * error;

    // Calculate if it is safe to deploy the parachute

    // First calculate if the lander is decelerating
    vector3d acceleration = calculate_acceleration();
    bool decelerating = (acceleration*velocity < 0);

    // Then check if it is safe in general and decelerating
    if (safe_to_deploy_parachute() && decelerating) {
        parachute_status = DEPLOYED;
    }

    // Calculate throttle
    if (P_out <= -delta_t) {
        throttle = 0;
    } else if (P_out > -delta_t && P_out < 1-delta_t) {
        throttle = P_out + delta_t;
    } else {
        throttle = 1;
    }
}