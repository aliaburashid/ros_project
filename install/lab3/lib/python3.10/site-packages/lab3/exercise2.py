import rclpy                              # Imports ROS2 Python client library
from rclpy.node import Node               # Imports base Node class
from geometry_msgs.msg import Twist       # Imports Twist message type for velocity
from rclpy.exceptions import ROSInterruptException
import signal                             # Used to catch Ctrl+C safely
import threading                          # Used to run spin() in a separate thread
import math                               # Used for pi and angle calculations


class SquareDriver(Node):
    def __init__(self):
        super().__init__('square_driver')  # Initializes ROS node with name

        # Creates publisher that sends Twist messages to /cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Creates a rate object to control publishing frequency (10 Hz)
        self.rate = self.create_rate(10)


    def move_straight(self, speed=0.15, seconds=2.0):
        """Moves robot forward at given speed for given time."""

        msg = Twist()                     # Creates empty Twist message
        msg.linear.x = speed              # Sets forward velocity (m/s)

        # Calculates number of loop iterations (10 Hz × seconds)
        steps = int(seconds * 10)

        for _ in range(steps):            # Repeats for required duration
            self.publisher.publish(msg)   # Publishes forward velocity
            self.rate.sleep()             # Maintains 10 Hz frequency


    def turn_left_90(self, ang_speed=0.8):
        """Rotates robot approximately 90 degrees left."""

        msg = Twist()                     # Creates empty Twist message
        msg.angular.z = ang_speed         # Sets angular velocity (rad/s)

        # Time needed to rotate 90 degrees: angle / angular velocity
        turn_time = (math.pi / 2.0) / ang_speed

        # Converts time to loop iterations (10 Hz)
        steps = int(turn_time * 10)

        for _ in range(steps):            # Repeats for calculated turn duration
            self.publisher.publish(msg)   # Publishes rotation command
            self.rate.sleep()             # Maintains 10 Hz frequency


    def stop(self):
        """Stops robot by sending zero velocities."""
        self.publisher.publish(Twist())   # Publishes empty Twist (all zeros)


def main(args=None):
    rclpy.init(args=args)                 # Initializes ROS2 communication

    node = SquareDriver()                 # Creates node instance

    # Defines function that runs when Ctrl+C is pressed
    def signal_handler(sig, frame):
        node.stop()                       # Ensures robot stops
        rclpy.shutdown()                  # Shuts down ROS cleanly

    signal.signal(signal.SIGINT, signal_handler)

    # Starts ROS spin in a background thread
    thread = threading.Thread(
        target=rclpy.spin,
        args=(node,),
        daemon=True
    )
    thread.start()

    try:
        # Runs continuously while ROS is active
        while rclpy.ok():

            for _ in range(4):            # Repeats 4 times (4 sides of square)

                node.move_straight()      # Drives forward
                node.stop()               # Brief stop for cleaner motion

                node.turn_left_90()       # Rotates 90 degrees left
                node.stop()               # Brief stop before next side

    except ROSInterruptException:
        pass

    finally:
        node.stop()                      # Final safety stop


if __name__ == '__main__':
    main()