#!/usr/bin/env python
# coding: utf-8

# In[13]:


#Loading packages

# System tools
import os
import argparse

# Data analysis
import pandas as pd

# Drawing
import networkx as nx
import matplotlib.pyplot as plt


# In[14]:


#Creating the main function

def main():
    
    # define input parameters
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_file", required=True, help="path to input file")
    ap.add_argument("-w", "--weight", required=True, help="edge weight")
    args = vars(ap.parse_args())
    
    # save input parameters
    input_file = args["input_file"]
    weight = args["weight"]
    
    # run network analysis
    Network_analysis(input_file, weight)


# In[15]:


#Network Analysis

class Network_analysis:
    
    def __init__(self, input_file, weight): 
        
        # Create output directories
        self.create_output_directory("output")
        self.create_output_directory("viz")
        
        # load the data
        weighted_edgelist = pd.read_csv(input_file)
        
        # Create the network graph 
        network_graph = self.network_graph(weighted_edgelist, weight)
        
        # Calculate centraliy measures
        centrality_measures = self.centrality_measures(network_graph)
        
    #Create ouput folder if it isn't there already
    def create_output_directory(self, directory_name):
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
    
    
    def network_graph(self, weighted_edges_df, weight):
        
        # Filter based on edge weight
        filtered_edges_df = weighted_edges_df[weighted_edges_df["weight"] > weight]
        
        # Create graph using nx package
        network_graph = nx.from_pandas_edgelist(filtered_edges_df, "nodeA", "nodeB", ["weight"])
        
        # Plot it
        pos = nx.nx_agraph.graphviz_layout(network_graph, prog = "neato")
        nx.draw(network_graph, pos, with_labels=True, node_size=20, font_size=10)
        
        # Saving network graph 
        plt.savefig("viz/network.png", dpi=300, bbox_inches="tight")
        return network_graph
        
    
    def centrality_measures(self, network_graph):
        
        # Calcualte centrality measures (Eigenvector, betweenness and degree)
        eigenvector_metric = nx.eigenvector_centrality(network_graph)
        betweenness_metric = nx.betweenness_centrality(network_graph)
        degree_metric = nx.degree_centrality(network_graph)
        
        # Saving the three metrics in a dataframe
        centrality_measures_df = pd.DataFrame({
            'degree':pd.Series(degree_metric),
            'betweenness':pd.Series(betweenness_metric),
            'eigenvector':pd.Series(eigenvector_metric)  
        }).sort_values(['degree', 'betweenness', 'eigenvector'], ascending=False)
        
        # saving the csv file
        centrality_measures_df.to_csv("output/centrality_measures.csv")
        


# In[16]:


# Define behaviour when called from command line
if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




