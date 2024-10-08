from tqdm import tqdm

with open("grid.txt") as f:
    min_start_lon,max_start_lon = map(float, f.readline().strip().split(","))
    min_start_lat,max_start_lat = map(float, f.readline().strip().split(","))
    min_trip_pickup_datetime,max_trip_pickup_datetime = map(int, f.readline().strip().split(","))
    x_unit = (max_start_lon - min_start_lon)/100
    y_unit = (max_start_lat - min_start_lat)/100
    z_unit = (max_trip_pickup_datetime - min_trip_pickup_datetime)/100
    grid_size = 100
    grid = [[[[] for i in range(100)] for j in range(100)] for k in range(100)]
    grid_total_amts = [[[0 for i in range(100)] for j in range(100)] for k in range(100)]
    lon_loc, lat_loc, time_loc = 0,0,0
    
    while s:=f.readline():
        if s.startswith("("):
            lon_loc, lat_loc, time_loc = eval(s.strip())
            Grid_Total_Amt = float(f.readline().strip())
            grid_total_amts[lon_loc][lat_loc][time_loc] = Grid_Total_Amt
        else:
            # line_s = f.readline()
            # print(line_s)
            Start_lon, Start_Lat, Trip_Pickup_DateTime,Total_Amt = s.strip().split(",")
            
            Start_lon = float(Start_lon)
            Start_Lat = float(Start_Lat)
            Trip_Pickup_DateTime = int(Trip_Pickup_DateTime)
            Total_Amt = float(Total_Amt)
            # print(Start_Lat, Start_lon, Trip_Pickup_DateTime, Total_Amt)
            grid[lon_loc][lat_loc][time_loc].append((Start_lon, Start_Lat, Trip_Pickup_DateTime, Total_Amt))
            
from datetime import datetime
def query_text_to_list(s):
    query_str_list = s.strip().split(",")
    low_x = float(query_str_list[0])
    up_x = float(query_str_list[1])
    low_y = float(query_str_list[2])
    up_y = float(query_str_list[3])
    low_time = int(datetime.strptime(query_str_list[4], "%Y-%m-%d %H:%M:%S").timestamp())*1000000000
    up_time = int(datetime.strptime(query_str_list[5], "%Y-%m-%d %H:%M:%S").timestamp())*1000000000
    # print(query_str_list)
    # print(low_time, up_time)
    return [low_x, up_x, low_y, up_y, low_time, up_time]
    

with open("queries.txt") as f:
    queries = f.readlines()
    struc_queries = list(map(query_text_to_list, queries))



def get_grid_loc(time, lon, lat, min_time = min_trip_pickup_datetime, max_time = max_trip_pickup_datetime, min_lon = min_start_lon, max_lon = max_start_lon, min_lat = min_start_lat, max_lat = max_start_lat, grid_size = 100):
    time_loc = int((time - min_time)/(max_time - min_time+0.000001)*grid_size)
    lon_loc = int((lon - min_lon)/(max_lon - min_lon+0.000001)*grid_size)
    lat_loc = int((lat - min_lat)/(max_lat - min_lat+0.000001)*grid_size)
    time_loc = time_loc - 1 if time_loc != 0 else 0
    lon_loc = lon_loc - 1 if lon_loc != 0 else 0
    lat_loc = lat_loc - 1 if lat_loc != 0 else 0
    return (lon_loc, lat_loc, time_loc)


def calc_fraction(i,j,k, low_x, up_x, low_y, up_y, low_time, up_time,):
    min_x = min_start_lon + (max_start_lon - min_start_lon)/100*i
    max_x = min_start_lon + (max_start_lon - min_start_lon)/100*(i+1)
    min_y = min_start_lat + (max_start_lat - min_start_lat)/100*j
    max_y = min_start_lat + (max_start_lat - min_start_lat)/100*(j+1)
    min_time = min_trip_pickup_datetime + (max_trip_pickup_datetime - min_trip_pickup_datetime)/100*k
    max_time = min_trip_pickup_datetime + (max_trip_pickup_datetime - min_trip_pickup_datetime)/100*(k+1)
    
    intersection = (min(max_x, up_x) - max(min_x, low_x)) * (min(max_y, up_y) - max(min_y, low_y)) * (min(max_time, up_time) - max(min_time, low_time))
    
    box_vol = (max_x - min_x) * (max_y - min_y) * (max_time - min_time)
    
    # print(intersection, box_vol)
    fraction = intersection/box_vol
    # print(fraction)
    
    
    # if min_x<low_x:
    #     x_per = (max_x - low_x)/(max_x - min_x)

    # else:
    #     x_per = (up_x - min_x)/(max_x - min_x)
    # x_per = max(0, x_per)
    # x_per = min(1, x_per)
    # if min_y<low_y:
    #     y_per = (max_y - low_y)/(max_y - min_y)
    # else:
    #     y_per = (up_y - min_y)/(max_y - min_y)
    # y_per = max(0, y_per)
    # y_per = min(1, y_per)
    # if min_time<low_time:
    #     time_per = (max_time - low_time)/(max_time - min_time)
    # else:
    #     time_per = (up_time - min_time)/(max_time - min_time)
    # time_per = max(0, time_per)
    # time_per = min(1, time_per)
    # print("x_max:", max_x, "x_min:", min_x, "y_max:", max_y, "y_min:", min_y, "time_max:", max_time, "time_min:", min_time)
    # print("x_up:", up_x, "x_low:", low_x, "y_up:", up_y, "y_low:", low_y, "time_up:", up_time, "time_low:", low_time)
    # print(x_per, y_per, time_per), abs(x_per*y_per*time_per)
    # return abs(x_per*y_per*time_per)
    return max(0, fraction)


class Query:
    def __init__(self, low_x, up_x, low_y, up_y, low_time, up_time):
        self.low_x = low_x
        self.up_x = up_x
        self.low_y = low_y
        self.up_y = up_y
        self.low_time = low_time
        self.up_time = up_time
        self.low_x_grid, self.low_y_grid, self.low_time_grid = get_grid_loc(low_time, low_x, low_y)
        self.up_x_grid, self.up_y_grid, self.up_time_grid = get_grid_loc(up_time, up_x, up_y)
        # low_x_grid = int((self.low_time - min_trip_pickup_datetime)/(max_trip_pickup_datetime - min_trip_pickup_datetime+0.000001)*grid_size)
        # up_x_grid = int((self.up_time - min_trip_pickup_datetime)/(max_trip_pickup_datetime - min_trip_pickup_datetime+0.000001)*grid_size)
        # low_y_grid = int((self.low_x - min_start_lon)/(max_start_lon - min_start_lon+0.000001)*grid_size)
        # up_y_grid = int((self.up_x - min_start_lon)/(max_start_lon - min_start_lon+0.000001)*grid_size)
        # low_time_grid = int((self.low_y - min_start_lat)/(max_start_lat - min_start_lat+0.000001)*grid_size)
        # up_time_grid = int((self.up_y - min_start_lat)/(max_start_lat - min_start_lat+0.000001)*grid_size)
        # self.low_x_grid = low_x_grid - 1 if low_x_grid != 0 else 0
        # self.up_x_grid = up_x_grid - 1 if up_x_grid != 0 else 0
        # self.low_y_grid = low_y_grid - 1 if low_y_grid != 0 else 0
        # self.up_y_grid = up_y_grid - 1 if up_y_grid != 0 else 0
        # self.low_time_grid = low_time_grid - 1 if low_time_grid != 0 else 0
        # self.up_time_grid = up_time_grid - 1 if up_time_grid != 0 else 0
    def get_low_x_grid(self):
        return self.low_x_grid
    def get_up_x_grid(self):
        return self.up_x_grid
    def get_low_y_grid(self):
        return self.low_y_grid
    def get_up_y_grid(self):
        return self.up_y_grid
    def get_low_time_grid(self):
        return self.low_time_grid
    def get_sum_grid_points_in_query(self,grid_points):
        # print(grid_points)
        sum = 0
        for grid_point in grid_points:
            if grid_point[0] >= self.low_x and grid_point[0] <= self.up_x and grid_point[1] >= self.low_y and grid_point[1] <= self.up_y and grid_point[2] >= self.low_time and grid_point[2] <= self.up_time:
                sum+=grid_point[3]
        return sum
    def exac_query(self):
        sum = 0
        # print(self.low_x_grid, self.up_x_grid, self.low_y_grid, self.up_y_grid, self.low_time_grid, self.up_time_grid)
        for i in range(self.low_x_grid, self.up_x_grid+1):
            for j in range(self.low_y_grid, self.up_y_grid+1):
                for k in range(self.low_time_grid, self.up_time_grid+1):
                    if i == self.low_x_grid or i == self.up_x_grid or j == self.low_y_grid or j == self.up_y_grid or k == self.low_time_grid or k == self.up_time_grid:
                        sum+=self.get_sum_grid_points_in_query(grid[i][j][k])
                    else:
                        sum += grid_total_amts[i][j][k]
        return sum
    def approx_query(self):
        sum = 0
        # print(self.low_x_grid, self.up_x_grid, self.low_y_grid, self.up_y_grid, self.low_time_grid, self.up_time_grid)
        for i in range(self.low_x_grid, self.up_x_grid+1):
            for j in range(self.low_y_grid, self.up_y_grid+1):
                for k in range(self.low_time_grid, self.up_time_grid+1):
                    if i == self.low_x_grid or i == self.up_x_grid or j == self.low_y_grid or j == self.up_y_grid or k == self.low_time_grid or k == self.up_time_grid:
                        sum += calc_fraction(i,j,k, self.low_x, self.up_x, self.low_y, self.up_y, self.low_time, self.up_time)*grid_total_amts[i][j][k]
                    else:
                        sum += grid_total_amts[i][j][k]
        return sum
    

if __name__ == "__main__":
    import sys
    exact = int(sys.argv[1])
    from time import time
    start = time()
    if exact == 0:
        for query in struc_queries:
            query = Query(*query)
            print(query.approx_query())
    elif exact == 1:
        for query in struc_queries:
            query = Query(*query)
            print(query.exac_query())
    else:
        for query in struc_queries:
            query = Query(*query)
            print(query.exac_query())
            print(query.approx_query())
            print()
    print("Time usage:",time()-start)

    # with open("exact_results1.txt", "w") as f:
    #     for query in tqdm(struc_queries):
    #         query = Query(*query)
    #         # print(query.exac_query())
    #         f.write(str(query.exac_query()) + "\n")
            
    # with open("approx_results1.txt", "w") as f:
    #     for query in tqdm(struc_queries):
    #         query = Query(*query)
    #         # print(query.approx_query())
    #         f.write(str(query.approx_query()) + "\n")
        