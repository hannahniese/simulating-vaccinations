For visualisation you can use grid.py. It works similar to the network model
but produces a txt file as output that can be animated with the Processing
file grid_graphics/grid_graphics.pde.
In the grid, every person that lives not on the boundary has exactly 8 
neighbours to which it has contact. To visualize the results, open 
grid_graphics.pde and write the filename of the created .txt file in the
variable filename (line 20). Red and yellow pixels represent infected people,
dark green pixels are immune people and purple pixels are the vaccinatad
people.
!!! The grid model is just for visualisation. It does have different parameters
than the network model. For all analysis the network model should be used !!!
