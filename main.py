import utility as utility
import loader as loader
import numpy as np


def main():

    # Paths to the data and solution files.
    vrp_file = "n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "n32-k5.sol"  # "data/n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    #print('solution',vrp_best_sol)####

    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution") 

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(
        nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(
        nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!

    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Nearest Neighbour Heuristic to generate VRP solutions.

    sol = []
    remaining_node = []
    for i in range(len(px)-1):
        remaining_node.append(i+1)

    while len(remaining_node)>0:
    #for i in range(3):
        tour=[]
        tour_capacity=capacity
        current_node=depot
        next_node=None
        while tour_capacity>0:
            dist_min=float('inf')
            #find the nearest node to depot
            for node in remaining_node:
                dist=utility.calculate_euclidean_distance(px,py,current_node,node)
                if(dist<dist_min):
                    dist_min=dist
                    next_node=node

            tour_capacity=tour_capacity-demand[next_node]
            if(tour_capacity>0 and len(remaining_node)>0):
                current_node=next_node
                tour.append(next_node)
                remaining_node.remove(next_node)
            else:
                break
        sol.append(tour)
    print("Nearest Neighbour VRP Heuristic Solution:")
    for i in range(len(sol)):
        print('Route #',i+1,': ',sol[i])
    return sol


def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Saving Heuristic to generate VRP solutions.
    routes=[]
    remaining_node = []
    for i in range(len(px)-1):
        remaining_node.append(i+1)

    #initialise routes
    for i in range(len(px)-1):
        routes.append([i+1])
    
    #all the savings
    saving={}
    for i in remaining_node:
        dist_i=utility.calculate_euclidean_distance(px,py,i,depot)
        for j in remaining_node:
            if(i!=j):
                dist_j=utility.calculate_euclidean_distance(px,py,depot,j)
                dist_ij=utility.calculate_euclidean_distance(px,py,i,j)
                saving[i,j]=dist_i+dist_j-dist_ij
    #print(saving)

    while len(remaining_node)>0:
        for route in routes:
            route_capacity=capacity-route[0]
            merged_node=None
            remaining_node.remove(route[0])
            while route_capacity>0 and len(remaining_node)>0:                
                i=route[len(route)-1]
                #print(i)
                biggest_saving=0
                for j in remaining_node:
                    if(j!=i):
                        if (biggest_saving<saving[(i,j)]):
                            biggest_saving=saving[(i,j)]
                            merged_node=j
                #print(merged_node)                
                route_capacity-=demand[merged_node]
                if(route_capacity>0):
                    route.append(merged_node)
                    routes.remove([merged_node])
                    remaining_node.remove(merged_node)    
                #print(remaining_node,route_capacity)
    print('Saving VRP Heuristic Solution:') 
    for i in range(len(routes)):
        print('Route #',i+1,': ',routes[i])               
    return routes

if __name__ == '__main__':
    main()
