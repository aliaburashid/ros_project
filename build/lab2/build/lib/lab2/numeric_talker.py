# Import ROS2 Python library
import rclpy

# Import Node base class
from rclpy.node import Node

# Import message types
from std_msgs.msg import String
from std_msgs.msg import Int8   # NEW message type for numeric publisher


# Create NumericTalker class (inherits from Node)
class NumericTalker(Node):

    def __init__(self):
        # Name the node
        super().__init__('numeric_talker')

        # Publisher 1: String publisher (original chatter)
        self.string_publisher = self.create_publisher(String, 'chatter', 10)

        # Publisher 2: Numeric publisher (new topic)
        self.numeric_publisher = self.create_publisher(Int8, 'numeric_chatter', 10)

        # Timer (runs every 0.5 seconds)
        timer_in_seconds = 0.5
        self.timer = self.create_timer(timer_in_seconds, self.talker_callback)

        # Counter starts at 0
        self.counter = 0


    def talker_callback(self):

        # ---------------------------
        # Publish String message
        # ---------------------------
        string_msg = String()
        string_msg.data = f'Hello World, {self.counter}'
        self.string_publisher.publish(string_msg)

        # ---------------------------
        # Publish Numeric message
        # ---------------------------
        numeric_msg = Int8()
        numeric_msg.data = self.counter
        self.numeric_publisher.publish(numeric_msg)

        # Log both messages
        self.get_logger().info(
            f'Publishing: {string_msg.data} | Numeric: {numeric_msg.data}'
        )

        # Increment counter
        self.counter += 1

        # Reset to 0 if it exceeds 127 (max Int8 value)
        if self.counter > 127:
            self.counter = 0


# Main function
def main(args=None):
    rclpy.init(args=args)

    numeric_talker = NumericTalker()

    rclpy.spin(numeric_talker)


if __name__ == '__main__':
    main()
