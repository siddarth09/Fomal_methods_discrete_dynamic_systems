import networkx as nx
import matplotlib.pyplot as plt
import re 

class BuchiAutomaton:
    def __init__(self,file_path):
        self.file=file_path.split(".")[0]
        self.states=set()
        self.initial_states=set()
        self.accepting_state=set() 
        self.transitions=[]
        self.adj_matrix={}
        self.print_output(file_path)
    
    
    def print_output(self,file_path):
        with open(file_path,'r') as file: 
            lines=file.readlines()
            
            current_state=None 
            for line in lines: 
                
                line=line.strip()
                print(line)
                
                state=re.match(r'([a-zA-Z0-9_]+):',line)
                
                if state:
                    current_state=state.group(1)
                    self.states.add(current_state)
                    
                    if "init" in current_state:
                        self.initial_states.add(current_state)
                        
                    if "accept" in current_state:
                        self.accepting_state.add(current_state)
                        
                transition_match = re.match(r':: \((.*?)\) -> goto ([a-zA-Z0-9_]+)', line)
                
                if transition_match: 
                    condition,target_state=transition_match.groups()
                    
                    self.transitions.append((current_state,target_state,condition))
                    
                    # print(f"Transition: {current_state} -> {target_state} on {condition}")
                    
                    if current_state not in self.adj_matrix:
                        self.adj_matrix[current_state]=[]
                    self.adj_matrix[current_state].append((target_state,condition))
                    
                    print(self.adj_matrix)
                
    def plot(self):
        G=nx.DiGraph() #Directed Graph
        
        for s in self.states:
            G.add_node(s)
            
        for source,dest,label in self.transitions:
            G.add_edge(source,dest,label=label)
            
        pos=nx.spring_layout(G)
        nx.draw(G,pos,with_labels=True,node_size=2000,font_size=10,node_color='y')
        edge_labels={
            (source,destination):label for source,destination,label in self.transitions
        }
        
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        plt.title("Buchi Automaton")
        plt.show()
        
    def accepting_words(self, num_words=3):
        print("Generating Büchi Accepting Words")
        accepting_words = []

        for _ in range(num_words):
            word = []
            state = list(self.initial_states)[0] if self.initial_states else None
            if not state:
                print("No initial state found")
                break 

            visited_states = {}
            infinite_loop_detected = False

            while True:
                if state in self.accepting_state:
                    visited_states[state] = visited_states.get(state, 0) + 1
                    # If an accepting state is visited infinitely often, stop
                    if visited_states[state] > 2:  
                        infinite_loop_detected = True
                        break

                if state in self.adj_matrix:
                    transitions = self.adj_matrix[state]
                    next_state, label = transitions[0]  # Always take the first available transition
                    word.append(label)
                    state = next_state
                else:
                    break

            if infinite_loop_detected:
                accepting_words.append(word)
                             
        with open(self.file+"_sol.txt", "w") as f:
            # Write to the file
            f.write("Hello, Professor!\n")
            f.write("Accepting Words are given below:\n")
            f.write(str(accepting_words))
        return accepting_words 
        
                
def main():
    file_path='specification4.txt'
    buchi=BuchiAutomaton(file_path) 
    buchi.plot()
    # accepting_states=int(input("Enter the number of accepting states you want:"))
    print("ACCEPTING Words:",buchi.accepting_words())
    
if __name__=='__main__':
    main()       