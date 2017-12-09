#pragma once
#include<Graph.h>

class Route;
class RouteSet
{
private:
	std::vector<Route*> routes_vec;
public:
	RouteSet();
	~RouteSet();
	std::vector<Route*> routes();
	bool has_vertex(Vertex *v);
	void add_route(Route *r);
	std::string to_string();
};

class Route {
private:
	Vertex* terminals_arr[2];
	std::vector<Vertex*> vertices_vec;
public:
	Route();
	~Route();
	Vertex** terminals();
	std::vector<Vertex*> vertices();
	void add_vertex(Vertex* v);
	void remove_terminal(int remove_start);
	bool has_vertex(Vertex* v);
	std::string to_string();
};