#include "RouteSet.h"
#include <string>


RouteSet::RouteSet()
{
}


RouteSet::~RouteSet()
{
}

std::vector<Route*> RouteSet::routes()
{
	return routes_vec;
}

bool RouteSet::has_vertex(Vertex * v)
{
	for (Route* r : routes_vec)
		if (r->has_vertex(v))
			return true;
	return false;
}

void RouteSet::add_route(Route * r)
{
	routes_vec.push_back(r);
}

std::string RouteSet::to_string()
{
	std::string str="RoutSet<";
	for (Route* r: routes_vec) {
		str.append(r->to_string());
		str.append("\n");
	}
	str.append(">");
	return str;
}

Route::Route()
{
}

Route::~Route()
{

}

Vertex ** Route::terminals()
{
	{
		if (vertices_vec.size() == 0)
			throw 1;
		terminals_arr[0] = vertices_vec.front();
		terminals_arr[1] = vertices_vec.back();
		return terminals_arr;
	}
}

std::vector<Vertex*> Route::vertices()
{
	return vertices_vec;
}

void Route::add_vertex(Vertex * v)
{
	if (vertices_vec.size() == 0) 
		vertices_vec.push_back(v);
	else if (vertices_vec.size() == 1) {
		if (vertices_vec[0]->is_neighbour(v))
			vertices_vec.push_back(v);
		else
			throw 1;
	}
	else
		if (vertices_vec[0]->is_neighbour(v))
			vertices_vec.insert(vertices_vec.begin(), v);
		else if ((*(--vertices_vec.end()))->is_neighbour(v))
			vertices_vec.insert(vertices_vec.end(), v);
		else
			throw 1;
}

void Route::remove_terminal(int remove_start)
{
	if (remove_start != 0)
		vertices_vec.erase(vertices_vec.begin());
	else
		vertices_vec.pop_back();
}

bool Route::has_vertex(Vertex * v)
{
	for (auto it = vertices_vec.begin(); it != vertices_vec.end(); it++)
		if (*it == v)
			return true;
	return false;
}

std::string Route::to_string()
{
	std::string str = "Route: ";
	for (Vertex* v : vertices_vec) {
		str.append(std::to_string(v->serial_number()));
		str.append(" ");
	}
	return str;
}
