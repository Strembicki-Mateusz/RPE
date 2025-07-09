import g2o
import numpy as np

def main():

    optimizer = g2o.SparseOptimizer()
    solver = g2o.BlockSolverX(g2o.LinearSolverDenseX())
    optimizer.set_algorithm(g2o.OptimizationAlgorithmLevenberg(solver))


    robot_poses = [(0, 0, 0), (2.1, 0, 0), (4.0, 0, 0)]
    landmark_poses = [(0.5, 1.0, 0), (3.0, -1.0, 0)]


    poses = {}
    landmarks = {}


    for i, pose in enumerate(robot_poses):
        vertex = g2o.VertexSE2()
        vertex.set_id(i)
        vertex.set_estimate(g2o.SE2(*pose))
        optimizer.add_vertex(vertex)
        poses[i] = vertex
    
    for i, pose in enumerate(landmark_poses, start=len(robot_poses)):
        vertex = g2o.VertexSE2()
        vertex.set_id(i)
        vertex.set_estimate(g2o.SE2(*pose))
        optimizer.add_vertex(vertex)
        landmarks[i] = vertex

    constraints = [
        (0, 1, (2.1, 0, 0)),
        (1, 2, (1.9, 0, 0)),
        (0, 3, (0.5, 1.0, 0)),
        (1, 3, (-1.5, 1.0, 0)),
        (1, 4, (1.0, -1.0, 0)),
        (2, 4, (-1.0, -1.0, 0))
    ]

    for i1, i2, constraint in constraints:
        edge = g2o.EdgeSE2()
        edge.set_vertex(0, optimizer.vertex(i1))
        edge.set_vertex(1, optimizer.vertex(i2))
        edge.set_measurement(g2o.SE2(*constraint))
        edge.set_information(np.eye(3))
        optimizer.add_edge(edge)



    optimizer.initialize_optimization()
    optimizer.optimize(10)


    for i in range(len(robot_poses) + len(landmark_poses)):
        vertex = optimizer.vertex(i)
        print(f"Pose {i}: {vertex.estimate().to_vector()}")

if __name__ == "__main__":
    main()
