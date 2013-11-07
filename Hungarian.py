import numpy

tight_edge=[]
edge_weight=[]
path_set=[]
match_edge={}
node_weight={}
free_vertex=[]


def main():
   global tight_edge
   global match_edge
   global node_weight
   global free_vertex
   global edge_weight
   print 'main'
   print "matching edge:{0})".format(match_edge)
   total_weight=0
   left_num=len(edge_weight)
   for key, value in match_edge.iteritems():
      total_weight += edge_weight[min(key,value)][max(key,value)-left_num]
   print total_weight

   print "node_weight:{0}".format(node_weight)
   print "remain free_vertex:{0}".format(free_vertex)
   exit()

def init():
    global free_vertex
    global edge_weight
    global tight_edge
    
    edge_weight=[[2,0,0,0],
                 [3,2,0,0],
                 [1,3,2,1],
                 [0,0,2,1]]

    #find the max weight and assign it to vertices left
    max_value=max(max(edge_weight))
    left_num=len(edge_weight)
    right_num=len(edge_weight[0])
    node_num=left_num+right_num
    median_line=[left_num, node_num]
    tight_edge=[[] for i in range(left_num)]
    for i in range(left_num):
	for j in range(right_num):	
    		tight_edge[i].append(0)
    for i in range(0, node_num):
        if i < left_num:
            node_weight[i]=max_value
        else:
            node_weight[i]=0
        free_vertex.append(i)            
    free_vertex=find_tight()
    free_vertex=modify_free_node()
    zero_weight_node=[]
    while True:
    	for free_node in free_vertex:
		if free_node not in free_vertex:
			continue
		if node_weight[free_node] != 0:
			free_vertex=modify_free_node()
		else:
			zero_weight_node.append(free_node)
			zero_weight_node=list(set(zero_weight_node))
			zero_weight_node.sort(key=int)
			free_vertex.sort(key=int)
			if zero_weight_node == free_vertex:
				False
				print "all free vertex weight are 0 now"
    				main()
				exit()

    
            
def find_tight():
    global free_vertex
    global edge_weight
    global path_set
    global tight_edge
    print 'find_tight function'
    left_num=len(edge_weight)
    right_num=len(edge_weight[0])
    for i in range(0, left_num):
        for j in range(0, right_num):
           k=left_num+j
           if tight_edge[i][j]!=0:
           	continue
           elif edge_weight[i][j]!=0: 
           	if node_weight[i]+node_weight[k]==edge_weight[i][j]:
                	tight_edge[i][j]=1
			print 'new tight edge: %d %d'%(i,k)
	                if (i in free_vertex) and (k in free_vertex):
        	        	print '%s and %s are free vertex, add to path'%(i,k)    
                		match_edge[i]=k
	                	tmp_path=[]
         	        	tmp_path.append(i)
                		tmp_path.append(k)
	                	path_set.append(tmp_path)   #path_set is a matrix every element is a path
        	        	print 'the path set', path_set
                	        free_vertex.remove(i)
	                        free_vertex.remove(k)
		                print 'free vertex', free_vertex
                	else:
                    		print 'find tight edge, two ending points are not all free'
                    		print 'enter extend_path'
	                        extend_path(i,k)   #more complicate, one or both are matching vertices
    		                break
    print "start modify node value"
    return free_vertex



def extend_path(node1, node2):
    global path_set
    global free_vertex
    global match_edge
    print 'extend_path'
    path_num=len(path_set)
    new_path1=[]
    new_path2=[]
    new_path3=[]
    new_path4=[]
    if (node1 in free_vertex) or (node2 in free_vertex):  
    	if node1 in free_vertex:
       	   free_node=node1
	   matching_node=node2
    	elif node2 in free_vertex:
           free_node=node2
           matching_node=node1
        else: 
           print "error in extend_path1"
           exit()


        for path_index in range(0, path_num):
           path=path_set[path_index]
           if matching_node in path:
               path_length=len(path)
               node_index=path.index(matching_node)
               if node_index!=0:
                  new_path1=path[0:node_index+1]
                  new_path1.append(free_node)
                  path_set.append(new_path1)
                  match_edge,free_vertex=find_augmenting(new_path1)
		  new_path1=list(set(new_path1))
               if node_index!=(len(path)-1):
                  new_path2=path[node_index:path_length]
                  new_path2.insert(0,free_node)                  
                  path_set.append(new_path2)
                  match_edge,free_vertex=find_augmenting(new_path2)
		  new_path2=list(set(new_path2))
	       if node_index == 0 or node_index == len(path)-1:
	 	  del path
	       

    else: #  (node1 not in free_vertex) and (node2 not in free_vertex):
        for path_index in range(0,path_num):
 	    path=path_set[path_index]
	    if node1 in path:
               path_length=len(path)
	       node_index=path.index(node1)
               new_path1=path[0:node_index+1]
	       new_path2=path[node_index:path_length]
               new_path2.reverse()
            if node2 in path:
               path_length=len(path)
               node_index=path.index(node2)
               new_path3=path[0:node_index+1]
               new_path4=path[node_index:path_length]
               new_path3.reverse()           
            new_path1_length=len(new_path1)
            new_path2_length=len(new_path2)
            new_path3_length=len(new_path3)
            new_path4_length=len(new_path4)
            if new_path1_length!=0 and new_path3_length!=0:
               tmp_path=new_path1+new_path3
               path_set.append(tmp_path)
               find_augmenting(tmp_path)
            if new_path2_length!=0 and new_path3_length!=0:
               tmp_path=new_path2+new_path3
               path_set.append(tmp_path)
               find_augmenting(tmp_path)
            if new_path1_length!=0 and new_path4_length!=0:
               tmp_path=new_path1+new_path4
               path_set.append(tmp_path)
               find_augmenting(tmp_path)
            if new_path2_length!=0 and new_path4_length!=0:
               tmp_path=new_path2+new_path4
               path_set.append(tmp_path)
               find_augmenting(tmp_path)


	       
def find_augmenting(path):
    global match_edge
    global free_vertex
    path_length=len(path)
    left_num=len(match_edge)
    if (path[0] in free_vertex) and (path[-1] in free_vertex):
       if path[0] < left_num:
          i = 0
          for i in range(0, path_length,2):
             even_node=path[i]
             odd_node=path[i+1]
             if even_node in free_vertex:
                free_vertex.remove(even_node)
	        match_edge[even_node]=odd_node
	     if i+2 < path_length-1:
		del match_edge[path[i+2]]
		free_vertex.append(path[i+2])
                print "delete {0} from match edge".format(path[i+2])
       else: # path[0] >= left num
          for i in range(0,path_lengt,2):
             odd_node=path[i]
             even_node=path[i+1]
             if even_node in free_vertex:
                free_vertex.remove(even_node)
                match_edge[even_node]=odd_node
                if match_edge.has_key(even_node):
                	new_free_node=match_edge[even_node]
                  	free_vertex.append(new_free_node)

  

               
    return match_edge,free_vertex

 
def modify_free_node():
    print 'modify_free_node'
    global free_vertex
    global node_weight
    global path_set
    global edge_weight
    free_vertex_counter=0
    left_num=len(edge_weight)
    free_vertex_num=len(free_vertex)
    path_num=len(path_set)
    visited_node=[]
    if free_vertex_num==0:
         print 'no more free_vertex, program is gonna over'
         print node_weight
         main()
    else:
	 for free_node in free_vertex:
	   if free_node not in free_vertex:
		continue
           print 'free_node checking', free_node
           #free_node=free_vertex[free_vertex_index]
           if (node_weight[free_node]!=0):            #as long as one free vertex isn't 0, contimnue
              print "free node {0} weight: {1} minus 1".format(free_node, node_weight[free_node])
	      node_weight[free_node]=node_weight[free_node]-1
              visited_node.append(free_node)
              #if free_vertex in path, left nodes -1, right nodes +1
              for path in path_set:
                 if free_node in path:
                    path_length=len(path)
                    for element_index in range(0, path_length):
                        element=path[element_index]
                        if element not in visited_node:
                         if element < left_num:
                            print "node {0} on left side, weight {1} -1\n".format(element, node_weight[element]),
                            node_weight[element]-= 1
                            visited_node.append(element)
                         else:
                            print "node {0} on right side, weight {1} +1\n".format(element, node_weight[element]),
                            visited_node.append(element)

                            node_weight[element]+= 1
                    
                   
              print "after modify, check tight again"
              free_vertex=find_tight() 
           elif node_weight[free_node]==0:  
               print 'free node {0} is not qualify for modify with weight {1}'.format(free_node, node_weight[free_node])
               print 'free vertex set', free_vertex
    return free_vertex 


    






if __name__ == "__main__":
    init()



