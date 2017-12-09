#pragma once
#include<Graph.h>
#include<RouteSet.h>

struct Individual {
	RouteSet routeset;
	std::pair <double, double> fitness;
};

RouteSet generate_random_routeset(Graph &transit_network, int min_route_length, int max_route_length, int n_routes);
std::pair<double, double> fitness(RouteSet &population_member, Graph &transit_network, int *demand_matrix);
RouteSet crossover(RouteSet &r1, RouteSet &r2);
bool repair(RouteSet &routeset, Graph &transit_network, int max_route_length);
void mutate(RouteSet &rs, Graph transit_network, int min_length, int max_length);
template <class T> bool has_element(std::vector<T> vec, T elem);


void seamo_iterate(Individual *population_array, int population_size, Graph &transit_network, int min_route_length,
	int max_route_length, int n_routes, int *demand);
void seed_population(Individual *population_array, int population_size, Graph &transit_network, int min_route_length,
	int max_route_length, int n_routes, int *demand);
