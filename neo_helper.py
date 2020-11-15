class NeoHelper:
    from py2neo import Graph, Node, NodeMatcher, Relationship

    def __init__(self):
        self.name = "NeoHelper"

    def connect_graph(self, username, password):
        graph = self.Graph("bolt://localhost:7687", user=username, password=password)
        self.graph = graph

    def query_who_acted_in(self, movie_title):
        query = '''
        MATCH (m:Movie)<-[:ACTED_IN]-(a:Actor)
        WHERE m.title = $movie_title
        RETURN a.name AS actor_names
        LIMIT 1000
        '''
        results = self.graph.run(query, movie_title=movie_title)
        return results

    def query_who_directed(self, movie_title):
        query = '''
        MATCH (m:Movie)<-[:DIRECTED]-(d:Director)
        WHERE m.title = $movie_title
        RETURN d.name AS director_name
        '''
        results = self.graph.run(query, movie_title=movie_title)
        return results

    def query_directed(self, director_name):
        query = '''
        MATCH (d:Director)-[:DIRECTED]->(m:Movie)
        WHERE d.name = $director_name
        RETURN m.title as movie_titles
        '''
        movies = []
        results = self.graph.run(query, director_name = director_name)

        for r in results:
            movies.append(r['movie_titles'])
        return movies

    def query_actor_acted_in(self, actor_name):
        query = '''
        MATCH (m:Movie)<-[:ACTED_IN]-(a:Actor)
        WHERE a.name = $actor_name
        RETURN m.title AS movie_title
        '''
        movies = []
        results = self.graph.run(query, actor_name = actor_name)
        
        for r in results:
            movies.append(r['movie_title'])
        return movies

    def query_acted_with(self, actor_name):
        query = '''
        MATCH (a1:Actor)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(a2:Actor)
        WHERE a1.name = $actor_name
        RETURN a2.name AS actor_names
        '''
        actors = []
        results = self.graph.run(query, actor_name=actor_name)
        
        for r in results:
            actors.append(r['actor_names'])

        return actors