from skmine.itemsets import LCM
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary
from sklearn.metrics import f1_score




def cover(T,I):
    return set(I).issubset(set(T))



def conceptual_clustering(transaction_data, patterns, lamda,varr):
    # Number of transactions
    num_transactions = len(transaction_data)
    
    # Number of user-provided patterns
    num_patterns = len(patterns)

    # Create a binary variable for each cluster
    y = LpVariable.dicts("y", [j for j in range(num_patterns)], 0, 1, LpBinary)

    # Create the ILP problem
    prob = LpProblem("ConceptualClustering", LpMaximize)

    # Objective function: Maximize  the size of the pattern
    
    prob +=  lpSum(y[j] * len(patterns[j]) for j in range(num_patterns)), "Objective"
    #
    # Constraint (1): Each transaction should be covered by exactly one pattern
    #
    for i in range(num_transactions):
        prob += lpSum(1*y[j] for j in range(num_patterns) if cover(transaction_data[i],patterns[j])) == varr, f"Transaction_Coverage_{i}"


    # Constraint (2): Number of clusters should be exactly lamda
    
    prob += lpSum(y[j] for j in range(num_patterns)) == lamda, "Number_of_Clusters"

    # Solve the ILP problem
    prob.solve()
    soltime=prob.solutionTime
    
    print("the solution time :",soltime)

    # Output the results
    clusters = []
    best_patterns=[]
    for j in range(num_patterns):
        if y[j].value() == 1:
            clusters.append([T  for T in transaction_data if cover(T,patterns[j])])
            best_patterns.append(patterns[j])

   
    return (clusters,best_patterns,soltime)

# Load dataset
transaction_data =[]
#path='dataset/tictactoefinal.txt'
path='dataset/zoofinal.txt'
#path='dataset/votefinal.txt'
#path='dataset/soybeanfinal.txt'
#path='dataset/primaryTumorfinal.txt'
#path='dataset/mushroomfinal.txt'
#path='dataset/lymphfinal.txt'
#path='dataset/hepatisisfinal.txt'
#path='dataset/annealfinal.txt'
#
#
with open(path,'r') as file:
    for line in file:
        et=line.split(" ")
        del et[-1]
        transaction_data.append([int (ee) for ee in et])
print("number of transactions: ",len(transaction_data))
print("from ",transaction_data[0], " ... to  ",transaction_data[len(transaction_data)-1])

# Run LCM algorithm
#
#
#
minsup=0
#
#
print("MinSupport = ",minsup,"( or ",int(minsup*100)," %)")

minsupp_val = int(minsup * len(transaction_data))
if minsupp_val==0:
    minsupp_val=1



lcm = LCM(min_supp=minsupp_val)

p = lcm.fit_transform(transaction_data)

patterns = [itemset for itemset in p["itemset"]]

varr=1

print("Number of  closed itemsets before filtering : ",len(patterns))
 


lamda = 2
     
print("number of cluster chosen :", lamda)

result_clusters = conceptual_clustering(transaction_data, patterns, lamda,varr)

# Print the result clusters
print("number of founded clusters : ",len(result_clusters[0]))
        
    
print("CPU = ",result_clusters[2])






#
#computing F1-score
#

pathscore="Groundtruth/zoo.txt"
#pathscore="Groundtruth/lymph.txt"
#pathscore="Groundtruth/primarytumor.txt"
#pathscore="Groundtruth/mushroom.txt"
#pathscore="Groundtruth/tictactoe.txt"
#pathscore="Groundtruth/soybean.txt"
#pathscore="Groundtruth/vote.txt"
#pathscore="Groundtruth/hepatisis.txt"
#pathscore="Groundtruth/anneal.txt"

    
 
GroundTruthdata=[]
with open(pathscore,'r') as file:
    for line in file:
        et=line.split(" ")
        last=int(et[-1])
        del et[-1]
        GroundTruthdata.append(([int(ee)+1 for ee in et],last))



binaryclasses=[]
for e in GroundTruthdata:
    for j in range(len(result_clusters[0])):
        if e[0] in result_clusters[0][j]:
            binaryclasses.append(j)
            break

realclasses=[e[1] for e in GroundTruthdata] 



      
print("F1-score = ", f1_score(realclasses,binaryclasses))  


