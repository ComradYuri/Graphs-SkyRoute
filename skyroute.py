from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

# Comprehensible list of all tourist attractions numbered from A to Z
landmark_string = ""
for key in landmark_choices.keys():
    landmark_string += (key + " - " + landmark_choices[key] + '\n')

# list of inaccessible stations. These are removed from the metro graph
stations_under_construction = ['Moody Centre', 'Olympic Village']


# opening function
def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)


# Main wrapper for SkyRoute
def skyroute():
    greet()
    new_route()
    goodbye()

# if start and end is not set it returns them. If they are set the user can choose to update start, end, or both
def set_start_and_end(start_point, end_point):
    if start_point is not None:
        change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or "
                             "'b' for 'both': ")
        if change_point == 'b':
            start_point = get_start()
            end_point = get_end()
        elif change_point == 'o':
            start_point = get_start()
        elif change_point == 'd':
            end_point = get_end()
        else:
            print("Oops, that isn't 'o', 'd', or 'b''...")
            set_start_and_end(start_point, end_point)
    else:
        start_point = get_start()
        end_point = get_end()
    return start_point, end_point


# Requests user input and returns landmark start string from landmark_choices
def get_start():
    start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
    if start_point_letter in landmark_choices.keys():
        start_point = landmark_choices[start_point_letter]
        print("You selected {} as your starting point.".format(start_point))
        return start_point
    else:
        print(" Sorry, that's not a landmark we have data on. Let's try this again")
        get_start()


# Requests user input and returns landmark destination string from landmark_choices
def get_end():
    end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
    if end_point_letter in landmark_choices.keys():
        end_point = landmark_choices[end_point_letter]
        print("You selected {} as your destination.".format(end_point))
        return end_point
    else:
        print("Sorry, that's not a landmark we have data on. Let's try this again")
        get_end()


# Prints shortest route if there is one. If there is no possible connection due to maintenance it prints that.
def new_route(start_point=None, end_point=None):
    start_point, end_point = set_start_and_end(start_point, end_point)
    if start_point == end_point:
        print("You are already at {}".format(start_point))
    else:
        shortest_route = get_route(start_point, end_point)
        if shortest_route:
            shortest_route_string = '\n'.join(shortest_route)
            print("The shortest metro route from {} to {} is:\n{}".format(start_point,
                                                                          end_point,
                                                                          shortest_route_string))
        else:
            print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(
                start_point, end_point))
    again()


# after every new_route is at the end the user is asked if he wants additional info
def again():
    answer = input("Would you like to see another route? Enter y/n: ")
    if answer == 'y':
        show_landmarks()
        new_route(start_point=None, end_point=None)
    elif answer == 'n':
        return
    else:
        print('That is not a valid input. Enter y/n: ')
        return again()


# Collect start and end stations from vc_landmarks with landmarks as keys and a list of stations as output.
# Then it creates a route between a and b and returns the shortest route (shortest is least amount of stations visited)
def get_route(start_point, end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []
    for start_station in start_stations:
        for end_station in end_stations:
            # if there is construction metro_system becomes new updated graph. Else vc_metro graph is used
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            # checks if there is a possible route with a depth first search
            if len(stations_under_construction) > 0:
                possible_route = dfs(metro_system, start_station, end_station)
                if possible_route is None:
                    return None
            # creates routes with the different start and end stations
            route = bfs(metro_system, start_station, end_station)
            if route:
                routes.append(route)
    # selects shortest route from list of routes.
    shortest_route = min(routes, key=len)
    return shortest_route


# shows landmarks
def show_landmarks():
    see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
    if see_landmarks == 'y':
        print(landmark_string)
    elif see_landmarks == 'n':
        return
    else:
        print('That is not a valid input. Enter y/n: ')


# if there is construction it updates the graph of the metro network. Returns updated_metro
def get_active_stations():
    updated_metro = vc_metro
    for station_under_construction in stations_under_construction:
        for current_station, neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set([])
    return updated_metro


# goodby message for user
def goodbye():
    print("Thanks for using SkyRoute!")


# main function
skyroute()
#print(get_active_stations())
