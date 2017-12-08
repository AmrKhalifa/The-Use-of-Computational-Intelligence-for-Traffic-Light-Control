#include<stdio.h>
#include <iostream>
#include<Graph.h>
#include<genetic.h>
#include<fstream>
#include<string>
#include<sstream>

#define DISTANCES_MAT_PATH "C:\\Users\\eltay\\Documents\\grad_project\\Mumford_UTRP\\CEC2013Supp\\Instances\\MandlTravelTimes.txt"

int main() {
	std::ifstream myfile(DISTANCES_MAT_PATH);
	std::string line;
	Graph transit_network;

	if (myfile.is_open() ){
		getline(myfile, line);
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
		myfile.seekg(0, std::ios::beg);
		int i = 0;
		while (getline(myfile, line)) {
			std::istringstream iss(line);
			
			for (int j = 0; j < i; j++) {
				std::string entry;
				iss >> entry;
				if (entry != "Inf") {
					int distance = std::atoi(entry.data());
					Edge* e = new Edge(distance, transit_network.get_vertex_by_number(i), transit_network.get_vertex_by_number(j));
					transit_network.add_edge(e);
				}
			}
			getline(myfile, line);// get the empty line
			i++;
		}
		RouteSet rs = generate_random_routeset(transit_network, 2, 8, 6);
		std::cout << rs.to_string();

		fitness(rs, transit_network);
	}
}