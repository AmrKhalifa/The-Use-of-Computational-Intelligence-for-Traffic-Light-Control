#pragma once
#include<Graph.h>
#include<RouteSet.h>

RouteSet generate_random_routeset(Graph &transit_network, int min_route_length, int max_route_length, int n_routes);
std::pair<int, int> fitness(RouteSet &population_member, Graph &transit_network);