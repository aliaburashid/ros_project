import rclpy
from rclpy.node import Node

# Message types
from std_msgs.msg import String
from std_msgs.msg import Int8   # NEW: numeric message type


class NumericListener(Node):
    def __init__(self):
        # Name of this node
        super().__init__('numeric_listener')

        # Subscriber 1: listens to String messages on /chatter
        self.string_subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

        # Subscriber 2: listens to Int8 messages on /numeric_chatter
        self.numeric_subscription = self.create_subscription(
            Int8,
            'numeric_chatter',
            self.numeric_callback,
            10
        )

        # Prevent unused variable warnings
        self.string_subscription
        self.numeric_subscription

    # Callback for /chatter
    def listener_callback(self, msg):
        self.get_logger().info(f'I heard (string): {msg.data!r}')

    # Callback for /numeric_chatter
    def numeric_callback(self, msg):
        self.get_logger().info(f'I heard (number): {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    listener = NumericListener()
    rclpy.spin(listener)


if __name__ == '__main__':
    main()
