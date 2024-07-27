import heapq
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

class BlockWorld:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.visited = set()

    def is_goal(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = []
        n = len(state)
        
        for i in range(n):
            if state[i]:
                for j in range(n):
                    if i != j:
                        new_state = [stack[:] for stack in state]
                        block = new_state[i].pop()
                        new_state[j].append(block)
                        successors.append(new_state)
        
        return successors

    def heuristic(self, state):
        h = 0
        for i, stack in enumerate(state):
            for j, block in enumerate(stack):
                if i >= len(self.goal_state) or j >= len(self.goal_state[i]) or block != self.goal_state[i][j]:
                    h += 1
        return h

    def a_star(self):
        priority_queue = []
        initial_tuple = self.state_to_tuple(self.initial_state)
        heapq.heappush(priority_queue, (0, self.initial_state, [self.initial_state]))
        self.visited.add(initial_tuple)
        
        while priority_queue:
            f, current_state, path = heapq.heappop(priority_queue)
            
            if self.is_goal(current_state):
                return path
            
            for successor in self.get_successors(current_state):
                successor_tuple = self.state_to_tuple(successor)
                if successor_tuple not in self.visited:
                    self.visited.add(successor_tuple)
                    g = len(path)
                    h = self.heuristic(successor)
                    f = g + h
                    heapq.heappush(priority_queue, (f, successor, path + [successor]))
                    
        return None

    def state_to_tuple(self, state):
        return tuple(tuple(stack) for stack in state)

def print_state(state, step):
    print(f"Step {step}:")
    for i, stack in enumerate(state):
        print(f"Stack {i+1}: {stack}")
    print()

def get_state_input(prompt):
    print(prompt)
    state = []
    num_stacks = int(input("Enter the number of stacks: "))
    for i in range(num_stacks):
        stack = input(f"Enter stack {i+1} (comma-separated, leave blank for empty): ").strip()
        state.append(stack.split(',') if stack else [])
    return state

# Get user input for initial and goal states
initial_state = get_state_input("Enter the initial state:")
goal_state = get_state_input("Enter the goal state:")

block_world = BlockWorld(initial_state, goal_state)
solution = block_world.a_star()

if not solution:
    print("No solution found.")
    exit()

# Print steps
print("Solution found:")
for step, state in enumerate(solution, start=1):
    print_state(state, step)

# Animation part with buttons
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.set_xlim(0.5, len(initial_state) * 2 + 0.5)
ax.set_ylim(0, max(len(stack) for stack in initial_state + goal_state) + 2)

current_step = [0]

def update_plot(step):
    ax.clear()
    ax.set_xlim(0.5, len(initial_state) * 2 + 0.5)
    ax.set_ylim(0, max(len(stack) for stack in initial_state + goal_state) + 2)
    
    current_state = solution[step]
    for i, stack in enumerate(current_state):
        x_position = i * 2 + 1  # Start from column 1
        bar = ax.bar(x_position, len(stack), width=1, align='center', color='blue')
        for j, block in enumerate(stack):
            ax.text(x_position, j + 0.5, block, ha='center', va='bottom', color='white')
    ax.set_title(f"Step {step + 1}")

def next_step(event):
    if current_step[0] < len(solution) - 1:
        current_step[0] += 1
        update_plot(current_step[0])
        fig.canvas.draw()

def prev_step(event):
    if current_step[0] > 0:
        current_step[0] -= 1
        update_plot(current_step[0])
        fig.canvas.draw()

ax_next = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_prev = plt.axes([0.1, 0.05, 0.1, 0.075])

btn_next = Button(ax_next, 'Next')
btn_next.on_clicked(next_step)

btn_prev = Button(ax_prev, 'Previous')
btn_prev.on_clicked(prev_step)

update_plot(current_step[0])
plt.show()
