import math
import random
import matplotlib.pyplot as plt


def cal_dis(dis, path):
    # calculate the length of the path
    length = 0
    for i in range(len(path) - 1):
        length += dis[path[i]][path[i + 1]]
    return length

# calculate the probability of each element in the pooling area using roulette wheel selection
def roulette(pooling):
    sum_num = sum(pooling)
    temp_num = random.random()
    probability = 0
    for i in range(len(pooling)):
        probability += pooling[i] / sum_num
        if probability >= temp_num:
            return i
    return len(pooling)


def construct_path(dis, pheromone, alpha, beta):
    # construct a new path based on distance and pheromone
    path = [0]
    cur_node = 0
    unvisited_stops = [i for i in range(1, len(dis))]
    for i in range(len(dis) - 1):
        roulette_pooling = []
        for stop in unvisited_stops:
            roulette_pooling.append(math.pow(pheromone[cur_node][stop], alpha) * math.pow(1 / dis[cur_node][stop], beta))
        index = roulette(roulette_pooling)
        cur_node = unvisited_stops[index]
        path.append(cur_node)
        unvisited_stops.pop(index)
    path.append(0)
    return path


def main(coord_x, coord_y, pop, iter, alpha, beta, pho, Q):
    """
    The main function
    :param coord_x: the x coordinates of bus stops
    :param coord_y: the y coordinates of bus stops
    :param pop: the number of ants
    :param iter: the maximum number of iterations
    :param alpha: the importance of pheromone
    :param beta: the importance of heuristic
    :param pho: evaporation rate
    :param Q: the constant
    :return:
    """
    # Step 1. Initialization of parameters
    stop_num = len(coord_x)  # the number of stops
    dis = [[0 for _ in range(stop_num)] for _ in range(stop_num)]  # distance matrix
    for i in range(stop_num):
        for j in range(i, stop_num):
            temp_dis = math.sqrt((coord_x[i] - coord_x[j]) ** 2 + (coord_y[i] - coord_y[j]) ** 2)
            dis[i][j] = temp_dis
            dis[j][i] = temp_dis
    pheromone = [[1 for _ in range(stop_num)] for _ in range(stop_num)]
    iter_best = []  # the shortest path of each iteration
    best_path = []
    best_length = 1e6

    # Step 2. Iteration
    for _ in range(iter):

        # Step 2.1. Construct ant solutions
        ant_path = []
        ant_path_length = []
        for i in range(pop):
            new_path = construct_path(dis, pheromone, alpha, beta)
            new_length = cal_dis(dis, new_path)
            ant_path.append(new_path)
            ant_path_length.append(new_length)
        iter_best_path_length = min(ant_path_length)
        if iter_best_path_length < best_length:
            best_length = iter_best_path_length
            best_path = ant_path[ant_path_length.index(iter_best_path_length)]
        iter_best.append(best_length)

        # Step 2.2. Update pheromone
        for i in range(stop_num):
            for j in range(i, stop_num):
                pheromone[i][j] *= (1 - pho)
                pheromone[j][i] *= (1 - pho)
        for i in range(pop):
            delta = Q / ant_path_length[i]
            path = ant_path[i]
            for j in range(stop_num):
                pheromone[path[j]][path[j + 1]] += delta
                pheromone[path[j + 1]][path[j]] += delta

    # Step 3. Sort the results
    x = [i for i in range(iter)]
    plt.figure()
    plt.plot(x, iter_best, linewidth=2, color='blue')
    plt.title("Convergence curve")
    plt.xlabel("Iterations")
    plt.ylabel('Global optimal value')
    plt.show()

    # plot convergence graph and display shortest distance (best path) obtained
    plt.figure()
    plt.scatter(coord_x, coord_y, color='black')
    for i in range(len(best_path) - 1):
        temp_x = [coord_x[best_path[i]], coord_x[best_path[i + 1]]]
        temp_y = [coord_y[best_path[i]], coord_y[best_path[i + 1]]]
        plt.plot(temp_x, temp_y, color='blue')
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        plt.title('Best optimal route')
    plt.show()
    return {'Best path': best_path, 'Shortest length': best_length}


if __name__ == '__main__':
    # Define the parameters
    alpha = 1
    beta = 1
    rho = 0.1            #pheromone (evaporation rate)
    pop = 100            #number of ants
    iter = 50
    #city_num = 30
    #min_coord = 0
    #max_coord = 100

    with open('./busc06.txt', 'r') as f:
        lines = f.readlines()
        coord_x = [float(line.split()[1]) for line in lines]
        coord_y = [float(line.split()[2]) for line in lines]
    #coord_x = [3.067425,3.067413,3.067353,3.070932,3.074978,3.075409,3.070571,
               #3.065650,3.066866,3.067788,3.071382,3.072480,3.070642,3.067917]
    #coord_y = [101.489754,101.487781,101.483390,101.481727,101.487225,101.490231,101.491649,
               #101.495211,101.500978,101.505803,101.500757,101.499791,101.496965,101.493165]
    print(main(coord_x, coord_y, pop, iter, alpha, beta, rho, 10))


