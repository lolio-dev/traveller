from itertools import permutations
from os import environ

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = environ.get("API_KEY")


def get_distance(origin, destination):
	url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}" \
		  f"&destinations={destination}" \
		  f"&units=metric" \
		  f"&key={API_KEY}"
	req = requests.get(url)

	return req.json()["rows"][0]["elements"][0]["distance"]["value"]


def get_cities_distances(cities):
	return [[get_distance(i, j) for j in cities] for i in cities]


cities = ['Nancy', 'Metz', 'Paris', 'Reims', 'Troyes']
distances = [[0, 56060, 384852, 245159, 244897], [59654, 0, 330652, 190959, 252002],
			 [385336, 330876, 0, 144433, 178705], [245222, 190762, 143199, 0, 126454],
			 [246957, 251543, 178184, 126427, 0]]

if not distances:
	distances = get_cities_distances(cities)
	print(distances)


def get_nearest_city(city, already_visited):
	dist_min = 100000000
	nearest_city_index = -1
	for i in range(len(already_visited)):
		if not already_visited[i]:
			d = distances[i][city]
			if d < dist_min:
				nearest_city_index = i
				dist_min = d
	return nearest_city_index


def voyageur_glouton():
	route = [0]
	n = len(distances)
	already_visited = [False for _ in range(n)]
	city = 0
	for i in range(n - 1):
		already_visited[city] = True
		next_city = get_nearest_city(city, already_visited)
		route.append(next_city)
		city = next_city
	route.append(0)
	return route


def get_route_distance(route):
	distance = 0
	for city in range(len(route)):
		if city != len(route) - 1:
			distance += distances[route[city]][route[city + 1]]
	return distance


def voyageur_force_brut():
	min_route = [i for i in range(len(cities))] + [0]
	dist_min = get_route_distance(min_route)
	for permutation in permutations(range(1, len(cities))):
		route = [0] + list(permutation) + [0]
		distance = get_route_distance(route)
		if distance < dist_min:
			dist_min = distance
			min_route = route
	return min_route


def show_route_distance(route):
	for city in route:
		print(cities[city], '->', end=' ')
	print(f"{get_route_distance(route)}m = {get_route_distance(route) / 1000}km")


show_route_distance(voyageur_force_brut())
show_route_distance(voyageur_glouton())
