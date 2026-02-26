# This code defines a ROS 2 node that sends a navigation goal to a robot using the NavigateToPose action.
# Import the ROS2 Python client library
import rclpy

# Import the ActionClient class to communicate with ROS2 actions
from rclpy.action import ActionClient

# Import the Node base class to create a ROS2 node
from rclpy.node import Node

# Import PoseStamped message type (commonly used for stamped poses in ROS)
from geometry_msgs.msg import PoseStamped

# Import the NavigateToPose action definition from Nav2
from nav2_msgs.action import NavigateToPose

# Import math functions to convert yaw (Euler angle) to quaternion
from math import sin, cos


# Define a class that inherits from Node to create a navigation client node
class GoToPose(Node):

    # Constructor of the node
    def __init__(self):

        # Initialise the ROS2 node with the name 'navigation_goal_action_client'
        super().__init__('navigation_goal_action_client')

        # Create an ActionClient that sends NavigateToPose goals
        # to the Nav2 action server called 'navigate_to_pose'
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    # Define a method to send a navigation goal
    def send_goal(self, x, y, yaw):

        # Create a new goal message for the NavigateToPose action
        goal_msg = NavigateToPose.Goal()

        # Set the reference coordinate frame for the goal (map frame)
        goal_msg.pose.header.frame_id = 'map'

        # Set the timestamp of the goal message to the current time
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        # ---------------- Position ----------------

        # Set the desired X position in the map
        goal_msg.pose.pose.position.x = x

        # Set the desired Y position in the map
        goal_msg.pose.pose.position.y = y

        # ---------------- Orientation ----------------

        # Convert yaw (Euler angle) into quaternion form (z component)
        # Quaternion z = sin(yaw / 2)
        goal_msg.pose.pose.orientation.z = sin(yaw / 2)

        # Convert yaw (Euler angle) into quaternion form (w component)
        # Quaternion w = cos(yaw / 2)
        goal_msg.pose.pose.orientation.w = cos(yaw / 2)

        # Wait until the Nav2 action server becomes available
        self.action_client.wait_for_server()

        # Send the goal asynchronously to the action server
        # Register a feedback callback to receive progress updates
        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Register a callback that handles the goal response (accepted/rejected)
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    # Callback executed when the action server responds to the goal request
    def goal_response_callback(self, future):

        # Retrieve the goal handle from the future result
        goal_handle = future.result()

        # Check whether the goal was accepted
        if not goal_handle.accepted:

            # Log a message if the goal was rejected
            self.get_logger().info('Goal rejected')
            return

        # Log a message if the goal was accepted
        self.get_logger().info('Goal accepted')

        # Request the final result asynchronously
        self.get_result_future = goal_handle.get_result_async()

        # Register a callback to process the result once available
        self.get_result_future.add_done_callback(self.get_result_callback)

    # Callback executed when the final navigation result is returned
    def get_result_callback(self, future):

        # Extract the result of the navigation action
        result = future.result().result

        # Log the navigation result
        self.get_logger().info(f'Navigation result: {result}')

    # Callback executed periodically while the robot is navigating
    def feedback_callback(self, feedback_msg):

        # Extract feedback data from the message
        feedback = feedback_msg.feedback

        # NOTE: Feedback fields can be accessed and used if needed.
        # These lines are commented but show how to access useful data.

        ## Access the current robot pose during navigation
        #current_pose = feedback_msg.feedback.current_pose
        #position = current_pose.pose.position
        #orientation = current_pose.pose.orientation

        ## Access other feedback fields
        #navigation_time = feedback_msg.feedback.navigation_time
        #distance_remaining = feedback_msg.feedback.distance_remaining

        ## Example logging (currently disabled)
        #self.get_logger().info(f'Current Pose: [x: {position.x}, y: {position.y}, z: {position.z}]')
        #self.get_logger().info(f'Distance Remaining: {distance_remaining}')


# Main entry point of the program
def main(args=None):

    # Initialise ROS2 communication
    rclpy.init(args=args)

    # Create an instance of the GoToPose node
    go_to_pose = GoToPose()

    # Send a navigation goal (example coordinates)
    # x = 5.55, y = 1.0, yaw = 0.0 radians
    go_to_pose.send_goal(8.31, -5.88, 0.0)

    # Keep the node alive to process callbacks and action responses
    rclpy.spin(go_to_pose)


# Standard Python entry point check
if __name__ == '__main__':
    main()