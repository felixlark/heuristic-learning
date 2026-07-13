"""Transparent CartPole policies used by the advanced benchmark."""


def baseline(observation):
    """React only to pole angle, ignoring cart motion."""
    _, _, angle, _ = observation
    return int(angle > 0)


def improved(observation):
    """Balance angle and angular velocity with a small cart-position guard."""
    position, velocity, angle, angular_velocity = observation
    score = 1.8 * angle + angular_velocity + 0.08 * position + 0.03 * velocity
    return int(score > 0)
