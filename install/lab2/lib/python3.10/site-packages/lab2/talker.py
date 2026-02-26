# Import the main ROS2 Python client library
import rclpy

# Import the Node class (we will inherit from this to create our own node)
from rclpy.node import Node

# Import the standard ROS message type "String"
from std_msgs.msg import String


# Define a class called Talker that inherits from the ROS2 Node class
class Talker(Node):

    # Constructor method (runs when we create the node)
    def __init__(self):

        # Call the parent Node constructor and give this node the name "talker"
        super().__init__('talker')

        # Create a publisher:
        # - Message type: String
        # - Topic name: 'chatter'
        # - Queue size: 10 (buffer for outgoing messages)
        self.publisher = self.create_publisher(String, 'chatter', 10)

        # Define how often the callback function should run (every 0.5 seconds)
        timer_in_seconds = 0.5

        # Create a timer that calls self.talker_callback every 0.5 seconds
        self.timer = self.create_timer(timer_in_seconds, self.talker_callback)

        # Initialise a counter variable (used to count messages)
        self.counter = 0


    # This function runs every time the timer triggers (every 0.5 seconds)
    def talker_callback(self):

        # Create a new String message object
        msg = String()

        # Set the message content using an f-string
        # It will look like: "Hello World, 0", "Hello World, 1", etc.
        msg.data = f'Hello World, {self.counter}'

        # Publish the message to the "chatter" topic
        self.publisher.publish(msg)

        # Log the message to the terminal (this does NOT publish it)
        self.get_logger().info(f'Publishing: {msg.data}')

        # Increase the counter by 1 for the next message
        self.counter += 1


# Main function (entry point of the program)
def main(args=None):

    # Initialise ROS2 communication
    rclpy.init(args=args)

    # Create an instance of the Talker node
    talker = Talker()

    # Keep the node running (it will keep responding to timer events)
    rclpy.spin(talker)


# This ensures the main() function runs when we execute the file
if __name__ == '__main__':
    main()
