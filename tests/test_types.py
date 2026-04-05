from anima_ew_cruise_missile.types import LayerAction, MissileState, desired_heading_deg, distance_to_target


def test_type_helpers():
    ms = MissileState(x=0.0, y=0.0, z=10.0, speed=1.0, heading_rad=0.0)
    assert distance_to_target(ms, 3.0, 4.0) == 5.0
    assert round(desired_heading_deg(ms, 1.0, 0.0), 3) == 0.0


def test_layer_action_values():
    action = LayerAction(ew_level=1.0, cyber_level=0.5, deception_level=0.25)
    assert action.ew_level >= action.cyber_level >= action.deception_level
