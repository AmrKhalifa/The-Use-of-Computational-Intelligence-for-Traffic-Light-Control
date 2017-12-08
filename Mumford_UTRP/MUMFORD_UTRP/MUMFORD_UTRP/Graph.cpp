#include "Graph.h"



Graph::Graph()
{
}


Graph::~Graph()
{
}

void Graph::add_vertex(Vertex *v)
{
	vertices_vec.push_back(v);
}

void Graph::add_edge(Edge * e)
{
	edges_vec.push_back(e);
}

const std::vector<Vertex*> Graph::vertices()
{
	return vertices_vec;
}

Vertex * Graph::get_vertex_by_number(int n)
{
	for (auto i = vertices_vec.begin(); i != vertices_vec.end(); i++) {
		if ((*i)->serial_number() == n) {
			return *i;
		}
	}
	throw 1;
	return nullptr;
}

const std::vector<Edge*> Graph::edges()
{
	return edges_vec;
}

int Graph::size() const
{
	return vertices_vec.size();
}

int Vertex::counter = 0;
Vertex::Vertex(int serial_number)
{
	serial = serial_number;
}

Vertex::~Vertex()
{
}

void Vertex::add_edge(Edge * e)
{
	edges_vec.push_back(e);
}

const std::vector<Edge*> Vertex::edges()
{
	return edges_vec;
}

int Vertex::serial_number() const
{
	return serial;
}

bool Vertex::is_neighbour(Vertex * v)
{
	for (auto i = edges_vec.begin(); i != edges_vec.end(); i++)
		if ((*i)->neighbour_of(this) == v)
			return true;
	return false;
}

int Vertex::distance_to(Vertex * v)
{
	for (auto i = edges_vec.begin(); i != edges_vec.end(); i++)
		if ((*i)->neighbour_of(this) == v)
			return (*i)->length();
	throw 1;
	return 0;
}

Edge::Edge(int length, Vertex *v1, Vertex *v2)
{
	this->length_ = length;
	vertices_arr[0] = v1;
	vertices_arr[1] = v2;
	v1->add_edge(this);
	v2->add_edge(this);

}

Vertex** Edge::vertices()
{
	return vertices_arr;
}

Vertex * Edge::neighbour_of(Vertex * v)
{
	return vertices_arr[0]==v? vertices_arr[1]: vertices_arr[0];
}

int Edge::length()
{
	return length_;
}
