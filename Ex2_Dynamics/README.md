# Exercicio 2

This folder contains the python file utilized to command a aquatic robot in a simulated environment.
The second exercise simulates a more realistic approach.
On pratical applications, we're not able to set velocities or a pose estimation instantly for the robot.
All we can do is activate motors with determined intensity.

As on the exercise before:
Through the user cammands, the robot should be able to follow the pipes present on the scene.
The deviation represented as the distance between the expected path and the one realized was plotted and stored.

## Funtions Utilized

The robot movement was induced by the keyboard keys:
	
* W, S for movement in the X-axis;
* A, D for movement in the Y-axis;
* Q, E for movement in the Z-axis;

The program, then translates the user commands into messages to be transmitted to the robotic device.

The main change, when compared to Exercicio 1, 
was the type of message transmitted to the device.

* msg = Float64MultiArray()

msg is, now, an array of float values varying from 0 to 1.
The vehicle girona500 has 5 motors, which can be controled by value stored on the vector's indexes

* indexes [0] and [1] induces acceleration in the x-axis;
* indexes [2] and [3] induces acceleration in the z-axis;
* index [4] induces acceleration in the y-axis;

OBS: Notice that angular velocity on the device can be induced by apllying different values to the motor indexes.

The message is set, according to the user commands and, then, published:

* pub.publish(msg)

Obs: Angular velocities can be comunicated through messages:

## Results Archieved

The contol of the robotic device was not easy to archive.
In order for it to follow the pipeline, a lot of cautious was needed.
Even gravity influenced the robotic device's movement.

Results were not positive.
High error rates were noticed easily through the benchmarking and were comproved on the plots.

The only succesful case was Pipefollowing on the basic scene.
Although the gravity made it's position descend, the scene was short and could be concluded without harm.

All other scenes didn't present good error rates

## Conclusion

In order to drive the robotic device through the pipeline, a more advanced control approach is needed.

## References
<http://www.irs.uji.es/uwsim/wiki/index.php?title=First_steps:_Interacting_with_UWSim>

### Class of Robotica em Rede, UnB 2016
### prof. Raul Marin
### Author: Pedro Henrique Suruagy Perruci --- 14/0158596
