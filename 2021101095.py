import sys
from prettytable import PrettyTable

reward_coords = [3, 1]
penalty_coords = [3, 2]
grid = [[0, 0, 0], [0, 'w', 0], [0, 0, 0], [0, 1, -1]]          # 'w' represents wall is present on that tile

def checkconvergence(dp, dp_prev):
    flag = True
    for i in range(0, 4):
        for j in range(0, 3):
            if (abs(dp[i][j]-dp_prev[i][j]) > 0.0001):
                flag = False
                break
        if (not flag):
            break
    if (not flag):
        for i in range(0, 4):
            for j in range(0, 3):
                print("Utility Row No. ", i, "\tColumn No. ", j, " = ", dp[i][j])
    return flag


def max_here(a, b, c, d):
    dict = {a: 'Up', b: 'Down', c: 'Right', d: 'Left'}
    l = [a, b, c, d]
    l.sort()
    return l[-1], dict[l[-1]]


def valid(grid, i, j):
    if ((i < 0 or i >= 4) or (j < 0 or j >= 3)):
        return 0
    if (grid[i][j] == 'w'):
        return 0
    else:
        return 1


def solve(grid, dp, step, discount):
    count = 0
    dp_prev = []
    policy = []
    for i in range(0, 4):
        l = []
        l1 = []
        for j in range(0, 3):
            l.append(0)
            l1.append('')
        dp_prev.append(l)
        policy.append(l1)

    while True:
        print("\n\nIteration = ", count, "\n")
        if (checkconvergence(dp, dp_prev)):
            print("\n\nValues Converge now")
            break
        for i in range(0, 4):
            for j in range(0, 3):
                dp_prev[i][j] = dp[i][j]
        for i in range(0, 4):
            for j in range(0, 3):
                if ((i == reward_coords[0] and (j == reward_coords[1] or j == penalty_coords[1])) or grid[i][j] == 'w'):
                    continue
                north_value = step
                south_value = step
                east_value = step
                west_value = step
                if (valid(grid, i+1, j)):
                    north_value += discount*dp_prev[i+1][j]
                else:
                    north_value += discount*dp_prev[i][j]
                if (valid(grid, i-1, j)):
                    south_value += discount*dp_prev[i-1][j]
                else:
                    south_value += discount*dp_prev[i][j]
                if (valid(grid, i, j+1)):
                    east_value += discount*dp_prev[i][j+1]
                else:
                    east_value += discount*dp_prev[i][j]
                if (valid(grid, i, j-1)):
                    west_value += discount*dp_prev[i][j-1]
                else:
                    west_value += discount*dp_prev[i][j]
                dp[i][j], policy[i][j] = max_here(0.7*north_value+0.15*east_value+0.15*west_value,
                                                  0.7*south_value+0.15*east_value+0.15*west_value,
                                                  0.7*east_value+0.15*north_value+0.15*south_value,
                                                  0.7*west_value+0.15*north_value+0.15*south_value)
        count += 1
    for i in range(0, 4):
        for j in range(0, 3):
            if (i == reward_coords[0] and j == reward_coords[1]):
                policy[i][j] = 'Reward'
                # dp[i][j] = 'Reward'
            elif (i == penalty_coords[0] and j == penalty_coords[1]):
                policy[i][j] = 'Penalty'
                # dp[i][j] = 'Penalty'
            elif (grid[i][j] == 'w'):
                policy[i][j] = 'Wall'
                # dp[i][j] = 'Wall'


    myTable1 = PrettyTable(["X", "0", "1", "2"])
    print("\n\nUtility of Each Cell is as Follows:")
    for i in range(len(dp)-1, -1, -1):
        myTable1.add_row([i, dp[i][0], dp[i][1], dp[i][2]])
    print(myTable1)

    myTable2 = PrettyTable(["X", "0", "1", "2"])
    print("\n\nPolicy is as Follows:")
    for i in range(len(policy)-1, -1, -1):
        myTable2.add_row([i, policy[i][0], policy[i][1], policy[i][2]])
    print(myTable2)
    return

dp = []
for i in range(0, 4):
    l1 = []
    for j in range(0, 3):
        if (i == reward_coords[0] and j == reward_coords[1]):
            l1.append(1)
        elif (i == penalty_coords[0] and j == penalty_coords[1]):
            l1.append(-1)
        else:
            l1.append(0)
    dp.append(l1)

step_cost = -0.04
discount_factor = 0.95
solve(grid, dp, step_cost, discount_factor)