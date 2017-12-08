#include<stdio.h>
#include <iostream>
#include<Graph.h>
#include<genetic.h>
#include<fstream>
#include<string>
#include<sstream>

#define DISTANCES_MAT_PATH "C:\\Users\\eltay\\Documents\\grad_project\\Mumford_UTRP\\CEC2013Supp\\Instances\\MandlTravelTimes.txt"
#define DEMAND_MAT_PATH "C:\\Users\\eltay\\Documents\\grad_project\\Mumford_UTRP\\CEC2013Supp\\Instances\\MandlDemand.txt"
int main() {
	std::ifstream distances_file(DISTANCES_MAT_PATH);
	std::ifstream demand_file(DEMAND_MAT_PATH);
	std::string line;
	Graph transit_network;

	if (distances_file.is_open() ){
		getline(distances_file, line);
		std::istringstream iss(line);
		int number_of_vertices= 0;
		Vertex* v;
		while (iss) {
			std::string entry;
			iss >> entry;
			if (!entry.empty()) {
				v = new Vertex(number_of_vertices);
				number_of_vertices++;
				transit_network.add_vertex(v);
			}
		}
		distances_file.seekg(0, std::ios::beg);
		int i = 0;
		while (getline(distances_file, line)) {
			std::istringstream iss(line);
			
			for (int j = 0; j < i; j++) {
				std::string entry;
				iss >> entry;
				if (entry != "Inf" && entry != "0") {
					int distance = std::atoi(entry.data());
					Edge* e = new Edge(distance, transit_network.get_vertex_by_number(i), transit_network.get_vertex_by_number(j));
					transit_network.add_edge(e);
				}
			}
			getline(distances_file, line);// get the empty line
			i++;
		}
		int *demand_matrix = new int[number_of_vertices*number_of_vertices];
		for (int j = 0; j < number_of_vertices; j++) {
			getline(demand_file, line);
			std::istringstream iss(line);
			for (int k = 0; k < number_of_vertices; k++) {
				std::string entry;
				iss >> entry;
				demand_matrix[j*number_of_vertices + k] = std::atoi(entry.data());
			}	
			getline(demand_file, line); // get the empty line
		}

		RouteSet rs = generate_random_routeset(transit_network, 2, 8, 6);
		std::cout << rs.to_string();

		auto x =fitness(rs, transit_network, demand_matrix);
	}
}