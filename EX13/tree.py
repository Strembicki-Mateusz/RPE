import py_trees
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

robot_position = "Start Pose"
carried_object = None

object_locations = {
    "Object1 Location": (1, 3),
    "Object2 Location": (4, 3),
    "Target Location": (7, 7),
    "Start Pose": (0, 0)
}

class MoveTo(py_trees.behaviour.Behaviour):
    def __init__(self, name, location):
        super().__init__(name)
        self.location = location
        self.finished = False

    def update(self):
        global robot_position
        if not self.finished:
            print(f"Moving to {self.location}.")
            time.sleep(1)
            robot_position = self.location
            self.finished = True
            return py_trees.common.Status.RUNNING
        else:
            print(f"Arrived at {self.location}.")
            return py_trees.common.Status.SUCCESS

class PickObject(py_trees.behaviour.Behaviour):
    def __init__(self, name, object_name):
        super().__init__(name)
        self.object_name = object_name
        self.finished = False

    def update(self):
        global carried_object
        if not self.finished:
            print(f"Picking up {self.object_name}.")
            time.sleep(1)
            carried_object = self.object_name
            self.finished = True
            return py_trees.common.Status.RUNNING
        else:
            print(f"Picked up {self.object_name}.")
            return py_trees.common.Status.SUCCESS

class PlaceObject(py_trees.behaviour.Behaviour):
    def __init__(self, name, target_location):
        super().__init__(name)
        self.target_location = target_location
        self.finished = False

    def update(self):
        global carried_object
        if not self.finished:
            print(f"Placing object at {self.target_location}.")
            time.sleep(1)
            carried_object = None
            self.finished = True
            return py_trees.common.Status.RUNNING
        else:
            print(f"Object placed at {self.target_location}.")
            return py_trees.common.Status.SUCCESS

def create_behavior_tree():
    root = py_trees.composites.Sequence("Pick and Place Sequence", memory=True)

    sequence_1 = py_trees.composites.Sequence("Pick and Place Object 1", memory=True)
    sequence_1.add_child(MoveTo("Move to Object 1", "Object1 Location"))
    sequence_1.add_child(PickObject("Pick Object 1", "Object1"))
    sequence_1.add_child(MoveTo("Move to Target Location 1", "Target Location"))
    sequence_1.add_child(PlaceObject("Place Object 1", "Target Location"))

    sequence_2 = py_trees.composites.Sequence("Pick and Place Object 2", memory=True)
    sequence_2.add_child(MoveTo("Move to Object 2", "Object2 Location"))
    sequence_2.add_child(PickObject("Pick Object 2", "Object2"))
    sequence_2.add_child(MoveTo("Move to Target Location 2", "Target Location"))
    sequence_2.add_child(PlaceObject("Place Object 2", "Target Location"))

    return_to_start = MoveTo("Return to Start Pose", "Start Pose")

    root.add_child(sequence_1)
    root.add_child(sequence_2)
    root.add_child(return_to_start)

    return py_trees.trees.BehaviourTree(root)

tree = create_behavior_tree()

fig, ax = plt.subplots(figsize=(8, 8))

def plot_scene():
    ax.clear()
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 8)
    ax.set_aspect('equal', 'box')

    for obj, (x, y) in object_locations.items():
        if "Object1" in obj:
            ax.plot(x, y, 'bo', markersize=10, label=obj)
        elif "Object2" in obj:
            ax.plot(x, y, 'go', markersize=10, label=obj)
        elif "Target" in obj:
            ax.plot(x, y, 'mo', markersize=10, label=obj)
        else:
            ax.plot(x, y, 'ko', markersize=10, label=obj)

    robot_pos = object_locations.get(robot_position, (0, 0))
    ax.plot(robot_pos[0], robot_pos[1], 'ro', markersize=12, label="Robot")

    ax.set_title(f"Robot Position: {robot_position} | Carried Object: {carried_object}")
    ax.legend(loc="upper left")
    plt.draw()

print("Starting Behavior Tree execution...\n")

while tree.root.status != py_trees.common.Status.SUCCESS:
    tree.tick()
    plot_scene()
    plt.pause(1)

    print(f"Robot status -> Position: {robot_position}, Carried Object: {carried_object}")
    print("\n---\n")

print("Behavior Tree execution completed.")
