# imu_to_joint_states.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
import math

class IMUToJointState(Node):
    # def __init__(self):
    #     super().__init__('imu_to_joint_state_node')

    #     self.subscription = self.create_subscription(
    #         Float32MultiArray,
    #         '/imu_angles',
    #         self.imu_callback,
    #         10
    #     )

    #     self.publisher = self.create_publisher(
    #         JointState,
    #         '/joint_states',
    #         10
    #     )
        

    #     self.get_logger().info('IMU to JointState node started.')

    # def imu_callback(self, msg):
    #     if len(msg.data) < 2:
    #         self.get_logger().warn('Received less than 2 angles in /imu_angles')
    #         return

    #     pitch_deg = msg.data[1]  # Y-axis → base_joint
    #     roll_deg  = msg.data[0]  # X-axis → rot_joint

    #     # pitch_rad = math.radians(pitch_deg)
    #     # roll_rad  = math.radians(roll_deg)

    #     joint_state = JointState()
    #     joint_state.header.stamp = self.get_clock().now().to_msg()
    #     joint_state.name = ['base_joint', 'rot_joint']
    #     joint_state.position = [pitch_deg, roll_deg]

    #     self.publisher.publish(joint_state)
    def __init__(self):
        super().__init__('imu_to_joint_state_node')

        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/imu_angles',
            self.imu_callback,
            10
        )

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.latest_roll = 0.0
        self.latest_pitch = 0.0

        # Timer: publish at 144 Hz
        self.timer = self.create_timer(1.0 /200.0, self.publish_joint_state)

        self.get_logger().info('IMU to JointState node started.')

    def imu_callback(self, msg):
        if len(msg.data) < 2:
            self.get_logger().warn('Received less than 2 angles in /imu_angles')
            return

        # Store latest values (assumed to be in radians)
        self.latest_roll = msg.data[0]
        self.latest_pitch = msg.data[1]

    def publish_joint_state(self):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['base_joint', 'rot_joint']
        joint_state.position = [self.latest_pitch, self.latest_roll]  # be consistent with joint mapping
        self.publisher.publish(joint_state)


def main(args=None):
    rclpy.init(args=args)
    node = IMUToJointState()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
