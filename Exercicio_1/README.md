# Exercicio 1

### Class of Robotica em Rede, UnB 2016
### prof. Alberto J. Alvares
### Author: Pedro Henrique Suruagy Perruci --- 14/0158596

## Objectives

This folder contains the python file utilized to command a aquatic robot in a simulated environment.
On this initial exercise, our main goal was to understand and apply how to move the robotic device in different scenarios.
Through the user cammands, the robot should be able to follow the pipes present on the scene.
The deviation represented as the distance between the expected path and the one realized was plotted and stored.

## Funtions Utilized

The robot movement was induced by the keyboard keys:
	
* W, S for movement in the X-axis;
* A, D for movement in the Y-axis;
* Q, E for movement in the Z-axis;

The program, then translates the user commands into messages to be transmitted to the robotic device.
The functions used in python were:

* msg = TwistStamped()
* msg.twist.linear.x, msg.twist.linear.y, msg.twist.linear.z

Which set Linear velocities to the robotic device simulated.
Then, publishes the command:

* pub.publish(msg)

Obs: Angular velocities can be comunicated through messages:

* msg.twist.angular.x, msg.twist.angular.y, msg.twist.angular.z

Though, they were not necessary to this exercise.

## Results Archieved

The robotic device could be controlled sucessfully.
The set of keys chosen madde possible to conduce it confortably to follow the pipes.
 
Although, even in the basic environment, errors were found in high intensity.
This resulted can be explained by the difficulty in observing small disturbances on the device's trajectory caused by the scenario.
Also, the ideal path could be easily lost, due to the difficult vizualization on the simulation.
The consequence can be seen on the resultsError.pdf plot, in wich some high intensity errors were reported and, then, corrected.


## Conclusion

Even though the robotic device could be controlled by the user, errors on the were pretty evident in all scenarios.
It's notable that human interaction is an unstable solution when trying to accomplish tasks with minimal amount of errors.

On future projects, we shall use the functions studyied here to implement an autonomous way for the robot to navigate through the Pipes.
It's expected that this approach reports way smaller amounts of error, as we may use the robot's sensors to guide it's path.
