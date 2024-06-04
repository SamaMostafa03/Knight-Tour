import random
import tkinter as tk
from PIL import Image, ImageTk
import time
dx = [2, 1, -1, -2, -2, -1, 1, 2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]
initX, initY ,boardSize = 0, 0, 8
populationSize ,generations = 50, 1000
NoOfgenerations = 0
maxFitness = []
class Chromosome:
    def __init__(self, genes=None):
        self.genes = genes if genes is not None else [random.randint(1, 8) for _ in range(boardSize * boardSize - 1)]
class Knight:
    def __init__(self, chromosome=None):
        self.x, self.y, self.steps, self.fitness = 0, 0, 0, 0
        self.path = [(self.x, self.y)]
        self.checkForward = random.randint(0, 1)
        self.chromosome = chromosome if chromosome is not None else Chromosome()
class ChessboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Visualization")
        #root_width , root_height= 800 , 800
        root.geometry(f"{1000}x{800}")
        image = Image.open("KnightTour.jpg")
        self.photo = ImageTk.PhotoImage(image.resize((1000, 800)))
        background_label = tk.Label(root, image=self.photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Labels for board size, initial X, and initial Y
        self.board_size_label = tk.Label(root, text="Board Size:", font=("Arial", 14), fg="white", bg="black",highlightthickness=1,highlightcolor="black")
        self.init_x_label = tk.Label(root, text="Initial X:", font=("Arial", 14), fg="white", bg="black",highlightthickness=1,highlightcolor="black")
        self.init_y_label = tk.Label(root, text="Initial Y:", font=("Arial", 14), fg="white", bg="black" , highlightthickness=1,highlightcolor="black")
        self.board_size_entry = tk.Entry(root, font=("Arial", 14),highlightthickness=2)
        self.init_x_entry = tk.Entry(root, font=("Arial", 14),highlightthickness=2)
        self.init_y_entry = tk.Entry(root, font=("Arial", 14),highlightthickness=2)
        self.start_button = tk.Button(root, text="Start Visualization", command=self.start_visualization, font=("Arial", 14),highlightcolor="black",highlightthickness=1)
        # Radio buttons for choosing the approach
        self.approach_var = tk.StringVar()
        self.backtrack_radio = tk.Radiobutton(text="Backtrack Approach", variable=self.approach_var, value="backtrack", font=("Arial", 13), selectcolor= "black" ,fg="white", bg="black")
        self.genetic_radio = tk.Radiobutton(text="Genetic Approach", variable=self.approach_var, value="genetic", font=("Arial", 13), selectcolor= "black" ,fg="white", bg="black")
        # Place the labels and entry widgets at the bottom
        self.board_size_label.place(x=10, y=700)
        self.init_x_label.place(x=220, y=700)
        self.init_y_label.place(x=420, y=700)
        self.board_size_entry.place(x=114, y=700, width=50)
        self.init_x_entry.place(x=291, y=700, width=50)
        self.init_y_entry.place(x=491, y=700, width=50)
        self.start_button.place(x=750, y=730)
        self.backtrack_radio.place(x=100, y=750)
        self.genetic_radio.place(x=300, y=750)        
    def start_visualization(self):
        self.root.withdraw()  # Hide the initial configuration window
        global new_window
        new_window = tk.Toplevel()  # Create a new window for visualization
        new_window.title("Knight's Tour Visualization")
        global canvas
        canvas = tk.Canvas(new_window, width=800, height=850, bg="white")
        canvas.pack()
        global boardSize, initX, initY
        boardSize = int(self.board_size_entry.get())
        initX = int(self.init_x_entry.get())
        initY = int(self.init_y_entry.get())
        # Draw the initial chessboard
        global square_size
        square_size = 800 // boardSize
        for i in range(boardSize):
            for j in range(boardSize):
                canvas.create_rectangle(j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size,fill="white" if (i + j) % 2 == 0 else "orange")
        self.solution_label = tk.Label(new_window, text=f"Generating a solution..", font=("Arial", 14),
                              fg="white", bg="black", highlightthickness=1, highlightcolor="black")
        self.solution_label.place(x=250, y=810) 
        #initialize the knight photo
        image = Image.open("knight.png")
        global photo
        photo = ImageTk.PhotoImage(image.resize((int(square_size), int(square_size))))      
        #run the Approach choice
        if self.approach_var.get() == "backtrack":
            self.visualize_backtrack_approach()
        else :
            self.visualize_genetic_approach()  
    def dfs(self,x,y,stepCount):
        grid[x][y] = stepCount
        # Draw the knight's current position
        canvas.delete("kn")
        canvas.delete("invalid")
        new_window.after(50)
        text_item = canvas.create_text((y + 0.5) * square_size, (x + 0.5) * square_size, text=str(stepCount), fill="black", font=("Arial", 10, "bold"), tags="steps")
        canvas.create_image(y*square_size, x*square_size, anchor=tk.NW, image=photo, tags="kn")       
        if stepCount == boardSize*boardSize:
            return 1
        new_window.update_idletasks()
        new_window.update()
        availableMoves = []
        for i in range(8):
            xi , yi = x + dx[i] , y + dy[i]
            if xi>=0 and yi>=0 and xi<boardSize and yi<boardSize and grid[xi][yi] == 0 :
                counter = 0
                for j in range(8):
                    xj , yj = xi + dx[j] , yi + dy[j]
                    if xj>=0 and yj>=0 and xj<boardSize and yj<boardSize and grid[xj][yj] == 0:
                        counter+=1
                availableMoves.append( (counter,xi,yi) )
        availableMoves.sort()
        for it in availableMoves:
            if self.dfs(it[1],it[2],stepCount+1) :
                return 1
        canvas.create_rectangle(x * square_size, y * square_size,(x + 1) * square_size, (y + 1) * square_size,fill="red", outline="red" , tags="invalid")                    
        canvas.delete(text_item)
        grid[x][y] = 0
        return 0          
    def visualize_backtrack_approach(self):
        start_time = time.time()
        global grid
        grid =[ [0 for i in range(boardSize)]for j in range(boardSize)] 
        if self.dfs(initX,initY,1):
            for i in range(boardSize):
                for j in range(boardSize):
                    print(grid[i][j] , end=" ")
                print()     
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.show_time_in_new_window(elapsed_time)        
    def visualize_genetic_approach(self):
        #run the genetic algorithm
        start_time = time.time()
        population = [Knight() for _ in range(populationSize)]
        for generation in range(generations):
            #update the window for the new generation
            new_window.update_idletasks()
            new_window.update()
            canvas.delete("kn")
            canvas.delete("steps")
            canvas.delete("invalid")
            #generate population paths
            for i in range(boardSize*boardSize - 1):
                for knight in population:  
                    legal = False
                    limit = 0
                    #check for all 8 moves of a knight untill a valid move is found
                    while not legal and limit < 8:
                        direction = knight.chromosome.genes[knight.steps]
                        knight.x += dx[direction - 1]
                        knight.y += dy[direction - 1]
                        if 0 <= knight.x < boardSize and 0 <= knight.y < boardSize:
                            legal = True
                            for i in range(len(knight.path)):
                                if knight.path[i] == (knight.x, knight.y):
                                    legal = False
                        if not legal : 
                            knight.x -= dx[direction-1]
                            knight.y -= dy[direction-1]
                            if knight.checkForward == 1:
                                knight.chromosome.genes[knight.steps] = (knight.chromosome.genes[knight.steps] % 8) + 1
                            else:
                                knight.chromosome.genes[knight.steps] = ((knight.chromosome.genes[knight.steps] + 6) % 8) + 1
                        limit += 1                  
                    knight.path.append((knight.x, knight.y))
                    knight.steps += 1
            #generate fitness for each knight
            knightsWithFitness = []
            for knight in population:
                legal = True
                knight.fitness = 0
                for i in range(len(knight.path)):
                    x = knight.path[i][0]
                    y = knight.path[i][1]
                    if not (0 <= x < boardSize and 0 <= y < boardSize):
                        legal = False
                    for j in range(i):
                        if knight.path[i] == knight.path[j]:
                            legal = False
                    if not legal:
                        break
                    knight.fitness += 1
                   
                knightsWithFitness.append( (knight.fitness , knight) )
            knightsWithFitness = sorted(knightsWithFitness , key= lambda x: x[0] , reverse= True)
            max_fit = knightsWithFitness[0][0]
            best_knight = knightsWithFitness[0][1]
           #gui : movement of best knight in the population
            legal = True
            for i in range(len(best_knight.path)):
                    x = best_knight.path[i][0]
                    y = best_knight.path[i][1]
                    if not (0 <= x < boardSize and 0 <= y < boardSize):
                        legal = False
                    for j in range(i):
                        if best_knight.path[i] == best_knight.path[j]:
                            legal = False                                             
                    if legal :
                        # Draw the knight's current position
                        canvas.create_text((x + 0.5) * square_size, (y + 0.5) * square_size,text=str(i+1), fill="black", font=("Arial", 10, "bold") , tags="steps")
                        canvas.create_image(x*square_size, y*square_size, anchor=tk.NW, image=photo, tags="kn")
                        # Update the canvas after each move
                        new_window.update_idletasks()
                        new_window.update()
                        canvas.delete("kn")
                    else :
                        # Draw the invalid move in red
                        canvas.create_rectangle(x * square_size, y * square_size,(x + 1) * square_size, (y + 1) * square_size,fill="red", outline="red" , tags="invalid")
                        break    
            #best fitness of the generation
            print(f"Generation {generation + 1} maximum fitness is {max_fit}")
            NoOfgenerations = generation+1
            maxFitness.append(max_fit)
            if max_fit == boardSize * boardSize:
                print(f"Done with {generation + 1} generations")
                end_time = time.time()
                elapsed_time = end_time - start_time
                self.show_time_in_new_window(elapsed_time)
                break
            #generate parents    
            parents = []
            count = 0
            for sol in knightsWithFitness:
                count+=1
                parents.append(sol[1])
                if count == 20:
                    break
            #generate children
            children = []
            desiredLengthForChildren = populationSize - len(parents)
            while len(children) < desiredLengthForChildren:
                parent1 = random.choice(parents).chromosome
                parent2 = random.choice(parents).chromosome
                #crossover
                mid = random.randint(0, boardSize*boardSize-1)
                newGenes = parent1.genes[mid:] + parent2.genes[:mid]
                childChromosome = Chromosome(newGenes)
                children.append(Knight(childChromosome))
            #new population
            parents.extend(children)
            population = parents    
            for knight in population:
                knight.x , knight.y , knight.steps , knight.fitness = initX , initY , 0, 0
                knight.path = [ (initX,initY) ]
                #mutation
                for i in range(len(knight.chromosome.genes)):
                    if random.random() < 0.01:
                        knight.chromosome.genes[i] = random.randint(1, 8)        
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.show_time_in_new_window(elapsed_time)                    
    def show_time_in_new_window(self, elapsed_time):
        self.solution_label.destroy()
        time_label = tk.Label(new_window, text=f"Solution is generated..Time taken: {elapsed_time:.5f} seconds", font=("Arial", 14),
                              fg="white", bg="black", highlightthickness=1, highlightcolor="black")
        time_label.place(x=150, y=810) 
if __name__ == "__main__":
    root = tk.Tk()
    chessboard_gui = ChessboardGUI(root)
    root.mainloop()