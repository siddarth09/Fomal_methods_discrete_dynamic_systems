# Büchi Automaton Implementation

## Overview
This program reads the output of **SPOT** from a given **.txt** file containing the description of a Büchi Automaton. It processes the automaton structure, extracts states, transitions, and visualizes the automaton as a graph. Additionally, it generates **accepting words** based on the user input.


## According the Specifications, LTL formulation is given below 

### The LTL formulas for each specification are:

  ### **1. Visit r1 at least once, never visit o1 or o2:**
    F(r1)&G(!o1&!o2)
   

  ### **2.Visit r1 infinitely often, never visit o1:**
    G(F(r1))&G(!o1)
   

  ### **3.If r1 is visited, stay in r1 forever and never visit o1:**
    G(r1->G(r1))&G(!o1)
  

  ### **4.Visit r1, then r2, then r3 in order (not necessarily immediately):**
    F(r1)&G(r1->F(r2))&G(r2->F(r3))
    
## Expected Output
### **1. Parsing the Input File**
- The program reads the `specification1.txt` file and prints each line.
- It extracts:
  - **States** (S)
  - **Initial States** (s0)
  - **Accepting States** (F)
  - **Transitions** (δ)
  
Example Console Output (if `specification1.txt` contains):
```
never { /* Fr1 & G(!o1 & !o2) */
T0_init:
  if
  :: ((!(o1)) && (!(o2)) && (r1)) -> goto accept_S0
  :: ((!(o1)) && (!(o2)) && (!(r1))) -> goto T0_init
  fi;
accept_S0:
  if
  :: ((!(o1)) && (!(o2))) -> goto accept_S0
  fi;
}
```

Corresponding program output:
```
T0_init:
Transition: T0_init -> accept_S0 on (!(o1)) && (!(o2)) && (r1)
Transition: T0_init -> T0_init on (!(o1)) && (!(o2)) && (!(r1))
accept_S0:
Transition: accept_S0 -> accept_S0 on (!(o1)) && (!(o2))
```

### **2. Automaton Visualization**
- The automaton is plotted using **NetworkX** and **Matplotlib**.
- **Nodes represent states** (initial, accepting, and normal states).
- **Edges represent transitions** labeled with their conditions.
- The graph is displayed using `plt.show()`.

### **3. Accepting Words Generation**
- The user is prompted to enter the number of **accepting words** to generate.
- The automaton simulates transitions from the initial state to an accepting state.
- It returns a sequence of **transition conditions** leading to acceptance.

Example:
```
Enter the number of accepting states you want: 2
ACCEPTING Words: [['(!(o1)) && (!(o2)) && (r1)'], ['(!(o1)) && (!(o2)) && (r1)']]
```

## How to Run the Program
### **Prerequisites**
- Python 3.x
- Required libraries:
  - `networkx`
  - `matplotlib`
  - `re`

Install dependencies using:
```sh
pip install networkx matplotlib
```

### **Execution**
Run the program using:
```sh
python3 siddarth_hw2.py
```

## File Structure
```
.
├── specification1.txt  # Input file containing automaton description
├── specification1_sol.txt #Output file containing accepting words
├── siddarth_hw2.py      # Python script to parse and visualize automaton
└── README.md           # Documentation
```

## Notes
- Ensure the input file is formatted correctly (as per **SPOT output** syntax).
- If an **initial state** is not found, the program will display an error.
- The graph may differ based on **spring layout positioning**, but it should match the SPOT visualization structurally.



> Note : specification4.txt takes a long time to compute the accepting states (causing my laptop to hang)