import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.exceptions import ROSInterruptException
import signal
import threading


class CircleDriver(Node):
    def __init__(self):
        super().__init__('circle_driver')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.rate = self.create_rate(10)  # 10 Hz

    def drive_circle(self):
        msg = Twist()
        msg.linear.x = 0.2    # forward
        msg.angular.z = 0.2   # turn (circle)
        self.publisher.publish(msg)

    def stop(self):
        self.publisher.publish(Twist())  # all zeros


def main(args=None):
    rclpy.init(args=args)
    node = CircleDriver()

    def signal_handler(sig, frame):
        node.stop()
        rclpy.shutdown()

    signal.signal(signal.SIGINT, signal_handler)

    thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            node.drive_circle()
            node.rate.sleep()
    except ROSInterruptException:
        pass
    finally:
        node.stop()


if __name__ == '__main__':
    main()