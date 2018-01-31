#pragma once
#include<vector>
class Vertex;
class Edge;

class Graph
{
private:
	std::vector<Vertex*> vertices_vec;
	std::vector<Edge*> edges_vec;

public:
	Graph();
	~Graph();
	void add_vertex(Vertex *v);
	void add_edge(Edge *e);
	const std::vector<Vertex*> vertices();
	Vertex* get_vertex_by_number(int n);
	const std::vector<Edge*> edges();
	int size() const;
};

class Vertex
{
private:
	int serial;
	std::vector<Edge*> edges_vec;
public:
	Vertex(int serial_number);
	~Vertex();
	void add_edge(Edge *e);
	const std::vector<Edge*> edges();
	int serial_number() const; 
	bool is_neighbour(Vertex *v);
	int distance_to(Vertex* v);
};

class Edge 
{
private:
	Vertex* vertices_arr[2];
	int length_;
public:
	Edge(int length, Vertex *v1, Vertex *v2);
	Vertex** vertices();
	Vertex* neighbour_of(Vertex* v);
	int length();
};