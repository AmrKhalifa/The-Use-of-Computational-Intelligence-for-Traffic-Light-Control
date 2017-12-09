#include<RouteSet.h>
#include<Graph.h>
#include<cstdlib>
#include<algorithm>

#include<string>
#include<iostream>

#define TRANSFER_DELAY 5
#define INFINITY 1000000

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
	while (chosen.size()< transit_network.size()) {
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
			un_modified++;
			if (un_modified == 2)
				break;
			std::random_shuffle(routes.begin(), routes.end());
			routes_it = routes.begin();
			un_modified = true;
		}
	}
	return (chosen.size() == transit_network.size());
}

RouteSet generate_random_routeset(Graph &transit_network, int min_route_length, int max_route_length, int n_routes) {
	std::vector<Vertex*> chosen;
	RouteSet generated_routeset;
	for (int i = 0; i < n_routes; i++) {
		Route* a_route = new Route();
		Vertex* start_vertex;
		int growing_forward = 1;
		int n_reversals = 0;
		int route_length = (rand() % (max_route_length - min_route_length)) + min_route_length;
		if (i == 0) {
			int start_node_number = rand() % transit_network.size();
			start_vertex = transit_network.get_vertex_by_number(start_node_number);
		}
		else {
			int x = rand()%chosen.size();
			start_vertex = chosen[x];
		}
		a_route->add_vertex(start_vertex);
		if (!has_element(chosen, start_vertex))
			chosen.push_back(start_vertex);
		//TODO this code does not respect min_route_length, FIX IT!!
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
	if (chosen.size() < transit_network.size())
		routeset_is_valid = repair(generated_routeset, transit_network, max_route_length);
	if (routeset_is_valid)
		return generated_routeset;
	for (Route* r: generated_routeset.routes())
		delete (r);
	return generate_random_routeset(transit_network, min_route_length, max_route_length, n_routes);
}

std::vector<Vertex*> * build_transport_graph(RouteSet r, Graph &transit_network) {
	Graph g;
	int n_nodes = transit_network.size();
	std::vector<Vertex*> *pools = new std::vector<Vertex*>[n_nodes];
	int serial = 0;
	for (Route* route : r.routes()) {
		Vertex *v1 = new Vertex(serial++);
		Vertex* v2;
		pools[route->vertices()[0]->serial_number()].push_back(v1);
		for (int i = 1; i < route->vertices().size(); i++) {//this will break on routes shorter than two nodes;
			v2 = new Vertex(serial++);
			pools[route->vertices()[i]->serial_number()].push_back(v2);

			Vertex *v1_in_transit_network = route->vertices()[i-1];
			Vertex *v2_in_transit_network = route->vertices()[i];
			Edge* e = new Edge(v1_in_transit_network->distance_to(v2_in_transit_network), v1, v2);

			v1 = v2;

		}
	}
	for (int i = 0; i < transit_network.size(); i++) {
		auto BusStop = pools[i];
		for (int j = 0; j < BusStop.size(); j++) {
			for (int k = 0; k < j; k++) {
				Edge* e = new Edge(TRANSFER_DELAY, BusStop[j], BusStop[k]);
			}
		}
	}
	return pools;
}
std::pair < double, double > fitness(RouteSet &population_member, Graph &transit_network, int *demand_matrix) {
	auto bus_stops = build_transport_graph(population_member, transit_network);
	std::pair<double, double> fitness_(0, 0);
	int n_bus_stops = transit_network.size();
	int n_nodes = 0;
	for (int i = 0; i < n_bus_stops; i++)
		n_nodes += bus_stops[i].size();
	int *distances = new int[n_nodes*n_nodes]();
	for (int i = 0; i < n_nodes*n_nodes; i++)
		distances[i] = INFINITY;
	for (int i = 0; i < n_nodes; i++)
		distances[i*n_nodes + i] = 0;
	for (int i = 0; i < n_bus_stops; i++)
		for (Vertex* v1 : bus_stops[i])
			for (Edge* e : v1->edges()) {
				Vertex* v2 = e->neighbour_of(v1);
				distances[v1->serial_number() + v2->serial_number()*n_nodes] = e->length();
			}
	for (int k = 0; k < n_nodes; k++)
		for (int i = 0; i < n_nodes; i++)
			for (int j = 0; j < n_nodes; j++)
				if (distances[i*n_nodes + k] + distances[k*n_nodes + j] < distances[i*n_nodes + j])
					distances[i*n_nodes + j] = distances[i*n_nodes + k] + distances[k*n_nodes + j];
	int *busstop_distances = new int[n_bus_stops*n_bus_stops];
	for (int i = 0; i < n_bus_stops; i++) {
		for (int j = 0; j < n_bus_stops; j++) {
			int min_distance = INFINITY;
			for (Vertex *v1 : bus_stops[i]) {
				for (Vertex *v2 : bus_stops[j]) {
					if (distances[v1->serial_number()*n_nodes + v2->serial_number()] < min_distance)
						min_distance = distances[v1->serial_number()*n_nodes + v2->serial_number()];
				}
			}
			busstop_distances[i*n_bus_stops + j] = min_distance;
		}
	}
	for (int i = 0; i < n_bus_stops*n_bus_stops; i++)
		busstop_distances[i] *= demand_matrix[i];
	int total_distance_travelled = 0;
	int total_demand = 0;
	for (int i = 0; i < n_bus_stops; i++)
		for (int j = 0; j < i; j++) {
			total_distance_travelled += busstop_distances[i*n_bus_stops + j];
			total_demand += demand_matrix[i*n_bus_stops + j];
		}
	fitness_.first = (double)total_distance_travelled/total_demand;
	int total_routes_length = 0;
	for (Route *r : population_member.routes()) 
		for (int i = 1; i < r->vertices().size(); i++)
			total_routes_length += r->vertices()[i - 1]->distance_to(r->vertices()[i]);
	fitness_.second = total_routes_length;
	return fitness_;
}

void update_scores(RouteSet &r1, RouteSet &r2, RouteSet &result, double *scores) {
	RouteSet parents[2] = { r1,r2 };
	int n_routes = r1.routes().size();
	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < n_routes; j++) {
			scores[i*n_routes + j] = 0;
			Route *r = parents[i].routes()[j];
			for (Vertex *v : r->vertices())
				if (!result.has_vertex(v))
					scores[i*n_routes + j] += 1;
			scores[i*n_routes + j] /= r->vertices().size();
		}
	}
}
bool have_common_vertex(RouteSet &rs, Route *r) {
	for (Vertex *v : r->vertices())
		if (rs.has_vertex(v))
			return true;
	return false;
}
RouteSet crossover(RouteSet &r1, RouteSet &r2) {
	RouteSet result;
	RouteSet parents[2] = { r1,r2 };
	std::vector<int> *routes_selected = new std::vector<int>[2];
	int n_routes = r1.routes().size();
	int seed_route = rand() % n_routes;
	result.add_route(r1.routes()[seed_route]);
	routes_selected[0].push_back(seed_route);
	double* routeset_scores = new double[n_routes*2]();
	int current_routeset = 0;
	for (int i = 1; i < n_routes; i++) {
		update_scores(r1, r2, result, routeset_scores);// this does unneccessary work by calculating scores for nodes that have
		double max_score = -INFINITY;									//already been added
		int route_to_add_index;
		for (int j = 0; j < n_routes;j++)
			if (routeset_scores[n_routes*current_routeset + j] > max_score && !has_element(routes_selected[current_routeset], j) &&
				have_common_vertex(result, parents[current_routeset].routes()[j])) {
				max_score = routeset_scores[n_routes*current_routeset + j];
				route_to_add_index = j;
			}
		result.add_route(parents[current_routeset].routes()[route_to_add_index]);
		routes_selected[current_routeset].push_back(route_to_add_index);
		current_routeset = 1 - current_routeset;
	}
	return result;
}