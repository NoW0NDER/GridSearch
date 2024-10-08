import pandas as pd
from  tqdm import tqdm
yellow_tripdata = pd.read_parquet('yellow_tripdata_2009-02.parquet')
intresting_cols = ["Trip_Pickup_DateTime", "Start_Lon", "Start_Lat","Total_Amt"]

intresting_data = yellow_tripdata[intresting_cols].dropna()

# delete the rows with lon not in the range of [-180, 180] and lat not in the range of [-90, 90]
# intresting_data = intresting_data[(intresting_data["Start_Lon"] >= -180) & (intresting_data["Start_Lon"] <= 180) & (intresting_data["Start_Lat"] >= -90) & (intresting_data["Start_Lat"] <= 90)]

min_start_lon = intresting_data["Start_Lon"].min()

max_start_lon = intresting_data["Start_Lon"].max()

min_start_lat = intresting_data["Start_Lat"].min()

max_start_lat = intresting_data["Start_Lat"].max()

#convert the date time to datetime object, and get the timestamp
intresting_data["Trip_Pickup_DateTime"] = pd.to_datetime(intresting_data["Trip_Pickup_DateTime"])

min_trip_pickup_datetime = intresting_data["Trip_Pickup_DateTime"].min().value

max_trip_pickup_datetime = intresting_data["Trip_Pickup_DateTime"].max().value

# print(min_start_lon, max_start_lon, min_start_lat, max_start_lat, min_trip_pickup_datetime, max_trip_pickup_datetime)

def get_grid_loc(time, lon, lat, min_time = min_trip_pickup_datetime, max_time = max_trip_pickup_datetime, min_lon = min_start_lon, max_lon = max_start_lon, min_lat = min_start_lat, max_lat = max_start_lat, grid_size = 100):
    time_loc = int((time.value - min_time)/(max_time - min_time+0.000001)*grid_size)
    lon_loc = int((lon - min_lon)/(max_lon - min_lon+0.000001)*grid_size)
    lat_loc = int((lat - min_lat)/(max_lat - min_lat+0.000001)*grid_size)
    time_loc = time_loc - 1 if time_loc != 0 else 0
    lon_loc = lon_loc - 1 if lon_loc != 0 else 0
    lat_loc = lat_loc - 1 if lat_loc != 0 else 0
    return (lon_loc, lat_loc, time_loc)
    

grid = [[[[] for i in range(100)] for j in range(100)] for k in range(100)]

for index, row in tqdm(intresting_data.iterrows(),total=intresting_data.shape[0]):
    grid_loc = get_grid_loc(row["Trip_Pickup_DateTime"], row["Start_Lon"], row["Start_Lat"])
    grid[grid_loc[0]][grid_loc[1]][grid_loc[2]].append((row["Start_Lon"], row["Start_Lat"],row["Trip_Pickup_DateTime"].value, row["Total_Amt"]))
    
    

    
    
    
with open("grid.txt", "w") as f:
    header = f"""{min_start_lon}, {max_start_lon}\n{min_start_lat}, {max_start_lat}\n{min_trip_pickup_datetime}, {max_trip_pickup_datetime}\n"""
    f.write(header)
    for i in range(100):
        for j in range(100):
            for k in range(100):
                f.write(f"({i},{j},{k})\n")
                total = sum([l[3] for l in grid[i][j][k]])
                print(total,[l[3] for l in grid[i][j][k]])
                f.write(f"{total}\n")
                for l in grid[i][j][k]:
                    f.write(f"{l[0]},{l[1]},{l[2]},{l[3]}\n")
                    
                    