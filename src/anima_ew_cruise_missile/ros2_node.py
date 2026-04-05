from __future__ import annotations


class EWCruiseMissileNode:
    """ROS2 integration skeleton.

    Designed as a stub for later deployment wiring on systems with rclpy.
    """

    def __init__(self) -> None:
        self.node_name = "ew_cruise_missile_defense_node"

    def setup(self) -> None:
        pass

    def process_message(self, payload: dict) -> dict:
        return {
            "node": self.node_name,
            "status": "stub",
            "echo": payload,
        }


def try_create_ros_node():
    try:
        import rclpy  # type: ignore
    except Exception:
        return EWCruiseMissileNode()

    # Placeholder branch for systems with ROS2 installed.
    _ = rclpy
    return EWCruiseMissileNode()
