import threading
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal


class Exercise2(Node):
    def __init__(self):
        super().__init__('exercise2')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz

    def move_in_square(self):
        desired_velocity = Twist()

        for i in range(4):
            desired_velocity.linear.x = 0.2  # Forward with 0.2 m/s
            desired_velocity.angular.z = 0.0
            for _ in range(30):  # Stop for a brief moment
                self.publisher.publish(desired_velocity)
                self.rate.sleep()

            desired_velocity.linear.x = 0.0
            desired_velocity.angular.z = (math.pi / 2) / 5

            for _ in range(50):  # Stop for a brief moment
                self.publisher.publish(desired_velocity)
                self.rate.sleep()

    def stop(self):
        desired_velocity = Twist()
        desired_velocity.linear.x = 0.0  # Send zero velocity to stop the robot
        self.publisher.publish(desired_velocity)

def main():
    def signal_handler(sig, frame):
        bot.stop()
        rclpy.shutdown()

    rclpy.init(args=None)
    bot = Exercise2()

    signal.signal(signal.SIGINT, signal_handler)
    thread = threading.Thread(target=rclpy.spin, args=(bot,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            bot.move_in_square()
    except ROSInterruptException:
        pass


if __name__ == "__main__":
    main()

