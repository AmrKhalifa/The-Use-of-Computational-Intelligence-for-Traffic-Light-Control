#include<RouteSet.h>
#include<Graph.h>
#include<cstdlib>
#include<algorithm>

#include<string>
#include<iostream>
#define TRANSFER_DELAY 5

template <class T> bool has_element(std::vector<T> vec, T elem) {
	for (auto it = vec.begin(); it != vec.end(); it++)
		if (*it ==elem)
			return true;
	return false;
}

bool repair(RouteSet &routeset, Graph &transit_network, int max_route_length) {
	//TODO Finish this function
	auto routes = routeset.routes();
	std::random_shuffle(routes.begin(), routes.end());
	std::vector<Vertex*> chosen;
	for (auto routes_it = routes.begin(); routes_it != routes.end(); routes_it++) {
		for (auto vertex: (*routes_it)->vertices())
			if (!has_element(chosen, vertex))
				chosen.push_back(vertex);
	}
	
	auto routes_it = routes.begin();
	int un_modified = 0;
	while (chosen.size()< transit_network.vertices().size()) {
		un_modified++;
		if ((*routes_it)->vertices().size() < max_route_length) {
			bool extended_first_terminal = false;
			Vertex** terminals = (*routes_it)->terminals();
			for (auto edge : terminals[0]->edges()) {
				Vertex* neighbour = edge->neighbour_of(terminals[0]);
				if (!has_element(chosen, neighbour)) {
					(*routes_it)->add_vertex(neighbour);
					chosen.push_back(neighbour);
					un_modified = 0;
					extended_first_terminal = true;
					break;
				}
			}
			if (!extended_first_terminal) {
				for (Edge* edge : terminals[1]->edges()) {
					Vertex* neighbour = edge->neighbour_of(terminals[1]);
					if (!has_element(chosen, neighbour)) {
						(*routes_it)->add_vertex(neighbour);
						chosen.push_back(neighbour);
						un_modified = 0;
						break;
					}
				}
			}
		}
		routes_it++;
		if (routes_it == routes.end()) {
			if (un_modified == 2)
				break;
			std::random_shuffle(routes.begin(), routes.end());
			routes_it = routes.begin();
			un_modified = true;
		}
	}
	return (chosen.size() == transit_network.vertices().size());
}

RouteSet generate_random_routeset(Graph &transit_network, int min_route_length, int max_route_length, int n_routes) {
	srand(685);
	std::vector<Vertex*> chosen;
	RouteSet generated_routeset;
	for (int i = 0; i < n_routes; i++) {
		Route* a_route = new Route();
		Vertex* start_vertex;
		int growing_forward = 1;
		int n_reversals = 0;
		int route_length = (rand() % (max_route_length - min_route_length)) + min_route_length;
		if (i == 0) {
			int start_node_number = rand() % transit_network.vertices().size();
			start_vertex = transit_network.get_vertex_by_number(start_node_number);
		}
		else {
			int x = rand()%chosen.size();
			start_vertex = chosen[x];
		}
		a_route->add_vertex(start_vertex);
		if (!has_element(chosen, start_vertex))
			chosen.push_back(start_vertex);
		while (n_reversals < 1 && a_route->vertices().size() < max_route_length) {
			Vertex* extending_terminal;
			std::vector<Vertex*> unused_neighbours;
			if (growing_forward)
				extending_terminal = a_route->terminals()[0];
			else
				extending_terminal = a_route->terminals()[1];
			for (Edge* edge : extending_terminal->edges())
				if (!a_route->has_vertex(edge->neighbour_of(extending_terminal)))
					unused_neighbours.push_back(edge->neighbour_of(extending_terminal));
			if (unused_neighbours.size() != 0) {
				int x = rand() % unused_neighbours.size();
				Vertex* to_add = unused_neighbours[x];
				a_route->add_vertex(to_add);//if the graph contains an isolated node this will not function correctly
				if (!has_element(chosen, to_add))
					chosen.push_back(to_add);
			}
			else {
				growing_forward = 0;
				n_reversals++;
			}
		}
		generated_routeset.add_route(a_route);
	}
	bool routeset_is_valid = true;
	if (chosen.size() < transit_network.vertices().size())
		routeset_is_valid = repair(generated_routeset, transit_network, max_route_length);
	if (routeset_is_valid)
		return generated_routeset;
	for (Route* r: generated_routeset.routes())
		delete (r);
	return generate_random_routeset(transit_network, min_route_length, max_route_length, n_routes);
}

std::vector<Vertex*> * build_transport_graph(RouteSet r, Graph &transit_network) {
	Graph g;
	int n_nodes = transit_network.vertices().size();
	std::vector<Vertex*> *pools = new std::vector<Vertex*>[transit_network.vertices().size()];
	int i = 0;
	for (Route* route : r.routes()) {
		Vertex *v1 = new Vertex(i++);
		Vertex *v2 = new Vertex(i++);
		pools[route->vertices()[0]->serial_number()].push_back(v1);
		for (int i = 1; i < route->vertices().size(); i++) {//this will break on routes shorter than two nodes;
			Vertex *v1_in_transit_network = route->vertices()[i-1];
			Vertex *v2_in_transit_network = route->vertices()[i];

			Edge* e = new Edge(v1_in_transit_network->distance_to(v2_in_transit_network), v1, v2);
			pools[route->vertices()[i]->serial_number()].push_back(v2);
			v1 = v2;
			v2 = new Vertex(i++);
		}
	}
	for (int i = 0; i < transit_network.vertices().size(); i++) {
		auto BusStop = pools[i];
		for (int j = 0; j < BusStop.size(); j++) {
			for (int k = 0; k < BusStop.size(); k++) {
				Edge* e = new Edge(TRANSFER_DELAY, BusStop[j], BusStop[k]);
			}
		}
	}
	return pools;
}
std::pair<int, int> fitness(RouteSet &population_member, Graph &transit_network) {
	auto bus_stops = build_transport_graph(population_member, transit_network);
	int n_nodes = 0;
	for (int i = 0; i < transit_network.vertices().size(); i++) 
		n_nodes += bus_stops[i].size();
	int *distances = new int[n_nodes*n_nodes];
	return std::pair<int, int>();
}