import numpy as np
import random
import os # For file name validation.

# Adjustable range constants for Z_percent and X_Percent
X_MAX = 30
X_MIN = 0
Z_MAX = 30
Z_MIN = 0

# Define a dictionary to store parameters
# Empty by Default.
parameterDictionary = {  
    "fileName": None,
    "PopulationSize": None,  # Number of Chromosomes in each generation.
    "numGenerations": None,  # Number of generations the algorithm will evolve.
    "X_Percent": None,  # Elitism rate/Percentage of chromosomes to be cloned without changes.
    "crossoverAlgorithm": "", # Type of crossover algorithm.
    "Z_Percent": None,  # Mutation rate/Probability of gene mutation (in percentage).
}

# Function to validate user input values for pop size, num gen, x & z percent.
def validateNumInput(prompt, errorMessage, inpCode, rateCode = 0): #default  rateCode = 0, case of no value.
  # inpCode tells what was input. Pop or gen input (code = 0). X% or Z% input (code = 1)
  # rateCode tells if it was X input (code = 0) or Z input (code = 1)
  while True:
    userInput = input(prompt)
    if userInput.isdigit() and int(userInput) > 0: # verifying + integer
      if inpCode == 0: # pop or gen input.
        return int(userInput)
      else: # X% or Z% input
        if rateCode == 0: # X% input
          if X_MIN <= int(userInput) <= X_MAX:
            return int(userInput)
        else: # Z% input
          if  Z_MIN <= int(userInput) <= Z_MAX:
            return int(userInput)
    print(errorMessage)
    

def setParameters(): # Use input statements to set parameter values
  global parameterDictionary
  print("Set Genetic Algorithm Parameters:")
  # Input validation for the filename
  while True:
    fileName = input("Enter the filename containing the training data: ")
    if fileName != "": # empty case, enter pressed without any user input.
      if os.path.isfile(fileName): #checks if the specified file exists in the file system.
        parameterDictionary["fileName"] = fileName
        break
      else:
        print("Error: File not found. Please enter a valid filename.\n")
    else:
      print("Error: Please enter a filename.\n")

  parameterDictionary["PopulationSize"] = validateNumInput(
    "Enter the population size: ",
    "Error: Population size must be a positive integer greater than zero!\n",
    0 # code for pop input
  )
  
  parameterDictionary["numGenerations"] = validateNumInput(
    "Enter the number of generations: ",
    "Error: Number of generations must be a positive integer greater than zero!\n",
    0 # code for gen input
  )

  parameterDictionary["X_Percent"] = validateNumInput( 
    "Enter the elitism rate: ",
    f"Error: Elitism rate should be a positive integer number and should be in the range [{X_MIN}, {X_MAX}]\n",
     1, 0 # code for X% input
  )

  # Input validation for the crossover algorithm
  while True:   # .strip() to remove leading and trailing whitespace, .lower() to make it non-case sensitive.
    crossoverAlgorithm = input("Enter the crossover algorithm (uniform or 1-point): ").strip().lower()
    if crossoverAlgorithm != "":
      if crossoverAlgorithm in ["uniform", "1-point"]:
        parameterDictionary["crossoverAlgorithm"] = crossoverAlgorithm
        break
      else:
        print("Error: Invalid crossover algorithm. Please enter 'uniform' or '1-point'.\n")
    else:
      print("Error: Please enter 'uniform' or '1-point'.\n")

  parameterDictionary["Z_Percent"] = validateNumInput( 
    "Enter the mutation rate: ",
    f"Error: Mutation rate should be a positive integer number and should be in the range [{Z_MIN}, {Z_MAX}]\n",
    1, 1 # code for Z% input
  )
  

  print("\nUsing the following parameters:\n")
  for key, value in parameterDictionary.items():
    print(f"{key}: {value}")


# Function to initialize a random chromosome
def initialize_chromosome():
  # Generate random values from a normal distribution with mean 0 and std deviation 1.15
  chromo = np.random.normal(loc=0, scale=1.15, size=4)
  # Round all the genes/floats in the chromosome to 2dp
  chromo = [np.round(genes, 2) for genes in chromo] 
  # Swap to ensure 1st < 2nd & 3rd < 4th
  if chromo[0] > chromo[1]:
    chromo[1],chromo[0] = chromo[0],chromo[1]
  if chromo[2] > chromo[3]:
    chromo[3],chromo[2] = chromo[2],chromo[3]
  # Randomly assign 0 or 1 to the final cell with a 50-50 probability.
  chromo = np.append(chromo, np.random.choice([0, 1]))
  #Numpy gives arrays, converting back to list: tolist()
  return chromo.tolist()


# Function to calculate the fitness score for a single line and chromosome
def FitnessFunction(chromosome, numberLine):
  FullMatch = False  # Flag to check for fully matched chromosome.
  # Checking if first and second number in data file in range of chromosome.
  if (numberLine[0] >= chromosome[0] and numberLine[0] <= chromosome[1]) and (numberLine[1] >= chromosome[2] and numberLine[1] <= chromosome[3]):
      FullMatch = True  # both numbers (1st, 2nd in line) from file in range.
  # numbers[-1] is the last element of the chromosome, which is the profit/loss.
  fitness = numberLine[-1]
  # If it's a full match, return the profit/loss to be added.
  if FullMatch:
    return fitness
  return 0  # No full match, no effect on fitness.


# Function to calculate the total fitness score for a given chromosome.
def totalFitnessCalculator(chromosome, lines_list):
  totalFitnessScore = 0
  matchFound = False  # Flag to check for a match in the whole file
  # Line by line totalFitnessScore is calculated & accumulated for a chromosome.
  for line in lines_list:
    fitness = FitnessFunction(chromosome, stringToFloatConverter(line))
    totalFitnessScore += fitness
    if fitness != 0:  # at least 1 Match found in the data from the file.
      matchFound = True
  # Not Match is always -5000
  if not matchFound:  # no match found in file.
    totalFitnessScore = -5000
  # last element of chromosome being 0 means SHORT (*-1).
  if totalFitnessScore != -5000 and chromosome[-1] == 0:  
    totalFitnessScore *= -1
  return totalFitnessScore


def stringToFloatConverter(line):
  # Takes a line and splits the line at whitespaces
  numbers = line.split()
  # Then converts every string in that line into a float using list comprehension.
  numbers = [float(number) for number in numbers]
  return numbers


def roulette_wheel_selection(currGen, totalFitnessScoresList):
  # Normalize results in the totalfitness score list by adding 5000 to all scores.
  totalFitnessScoresList = [score + 5000 for score in totalFitnessScoresList]
  # sum totalFitnessScore of every chromosome in the currGen.
  cumulativeFitnessScoreCurrGen = sum(totalFitnessScoresList)  
  # Generate a random selection point on the wheel b/w 0 and total fitness of pop.
  select_point = random.uniform(0, cumulativeFitnessScoreCurrGen)
  
  current_sum = 0
  # enumerate allows direct access to both index and chromosome.
  for index, chromosome in enumerate(currGen):  # enumerate keeps track of index stored in variable index.
    current_sum += totalFitnessScoresList[index]
    if current_sum >= select_point:
      return chromosome  # chromosome selected as parent
  # If for some reason no chromosome was selected, return the last one
  return currGen[-1]


def uniformCrossover(p1, p2):
  # child chromosome represented as an empty list.
  child = []
  # iterating 5 times for the 5 genes.
  for i in range(5):
    # Randomly select values from parent1 (0) and parent2 (1) to create child chromosome.
    select = random.choice([0, 1])
    if select == 0:
      child.append(p1[i])  # add from parent 1
    else:
      child.append(p2[i])  # add from parent 2  
  # Swap to ensure 1st < 2nd & 3rd < 4th
  if child[0] > child[1]:
    child[1],child[0] = child[0],child[1]
  if child[2] > child[3]:
    child[3],child[2] = child[2],child[3]
  return child


def onePointCrossover(p1, p2):
  # Initialize the child chromosome as an empty list
  child = []
  # Choose a random crossover point between 1 and 3
  crossover_point = random.randint(1, 3)
  # Copy upto first two genes from the first parent (p1)
  child.extend(p1[:crossover_point])
  # Copy the last three genes from the second parent (p2)
  child.extend(p2[crossover_point:])
  # Swap to ensure 1st < 2nd & 3rd < 4th
  if child[0] > child[1]:
    child[1],child[0] = child[0],child[1]
  if child[2] > child[3]:
    child[3],child[2] = child[2],child[3]
  return child


# Mutate the genes (values) of a chromosome with a specified mutation probability.
def mutateChromosome(child):
  # Iterate over first 4 values/genes in child chromosome for potential mutation.
  # If random % <= to Z%, meaning in range of mutation, mutate gene.
  for i in range(4):  
    if random.randint(1, 100) <= parameterDictionary["Z_Percent"]:  #Z% = Mutation probability.
      # np gives an array (temp). 
      temp = np.random.normal(loc=0, scale=1.15, size=1)
      # First element of that array is stored in the child list.
      child[i] = np.round(temp[0], 2) # rounded to 2 dp
  # Ensure that the genes are sorted: 1st < 2nd, 3rd < 4th
  if child[0] > child[1]:
    child[1],child[0] = child[0],child[1]
  if child[2] > child[3]:
    child[3],child[2] = child[2],child[3]
  return child


def createNextGen(currGenList, linesList):
  # Elitist Selection: Calculate the number of chromosomes to clone without changes (X%).
  # totalFitnessScoresList stores the total Fitness score of every chromosome in the currGen.
  totalFitnessScoresList = [totalFitnessCalculator(chromosome, linesList) for chromosome in currGenList]
  # Sort Curr gen in descending order to grab first x% of chromosome.
  for i in range(len(totalFitnessScoresList)):
    for j in range(i, len(totalFitnessScoresList)):
      if totalFitnessScoresList[i] < totalFitnessScoresList[j]:
        # Swap list[i] and list[j] to sort in descending order
        totalFitnessScoresList[i], totalFitnessScoresList[j] = totalFitnessScoresList[j], totalFitnessScoresList[i]
        currGenList[i], currGenList[j] = currGenList[j], currGenList[i]
  # Calculate num of clones based on the X_Percent parameter and the population size
  numClones = int(len(currGenList) * parameterDictionary["X_Percent"] / 100)
  nextGenList = []
  # Clone the top X% of chromosomes without changes
  nextGenList.extend(currGenList[:numClones])
  # Calculate the number of new chromosomes to be created (PopulationSize - num_clones)
  numNewChromosomes = parameterDictionary["PopulationSize"] - numClones
  # Creation of new chromosomes
  for _ in range(numNewChromosomes):  #_ placeholder, as value not needed in loop.
    # Select parents using roulette wheel selection
    parent1 = roulette_wheel_selection(currGenList, totalFitnessScoresList)
    parent2 = roulette_wheel_selection(currGenList, totalFitnessScoresList)
    # Perform crossover (choose either uniform or onePoint based on user input to create child)
    if parameterDictionary["crossoverAlgorithm"] == "uniform":
      child = uniformCrossover(parent1, parent2)
    else:
      child = onePointCrossover(parent1, parent2)
    # Apply mutation with Z% probability on child
    child = mutateChromosome(child)
    # Round all the genes/floats in the child chromosome to 2dp
    child = [np.round(genes, 2) for genes in child]
    # add child to the next gen list.
    nextGenList.append(child)  
  return nextGenList


def calculatefitnessStats(currGenPop, generationNum, linesList):
  # Calculate totalFitnessScore of every chromosome in the currGen and store it totalFitnessScores.
  totalfitnessScoresList = [totalFitnessCalculator(chromosome, linesList) for chromosome in currGenPop]
  # Track fitness statistics for each generation
  maxFitness = max(totalfitnessScoresList)
  minFitness = min(totalfitnessScoresList)
  meanFitness = sum(totalfitnessScoresList) / len(currGenPop)
  # Median calculation
  # Sort the fitness scores: Ascending order
  sortedFitness = sorted(totalfitnessScoresList)  
  n = len(sortedFitness)
  # Find middle index, taking into account index 0
  middleIndex = (n - 1) // 2 
  if n % 2 == 0:  # If the list has an even number of elements, average the middle two
    medianFitness = np.round((sortedFitness[middleIndex] + sortedFitness[middleIndex + 1]) / 2, 2)
  else:
    medianFitness = np.round(sortedFitness[middleIndex], 2)
    
  print("\n*****************************")
  print("Statistics After: Generation", np.round(generationNum, 2))
  print("Max Fitness:", np.round(maxFitness, 2))
  print("Min Fitness:", np.round(minFitness, 2))
  print("Average Fitness (Mean):", np.round(meanFitness, 2))
  print("Median Fitness:", np.round(medianFitness, 2))
  print("*****************************\n")


def displayHighestFitness(currGenPop, linesList):
  # Find and display the highest fitness chromosome from the final generation.
  highestFitnessChromosome = max(currGenPop, key=lambda chromosome: totalFitnessCalculator(chromosome, linesList))
  print("\nHighest Fitness Chromosome from the Final Generation:")
  print("Chromosome:", highestFitnessChromosome)
  print("Fitness Score:", np.round(totalFitnessCalculator(highestFitnessChromosome, linesList), 2))


def main():
  print("Genetic Algorithm : 2-day chart patterns in financial data\n")
  # User interface to set parameters.
  setParameters() 
  with open(parameterDictionary["fileName"], "r") as file:
    # Read all lines in the file as a list of strings.
    linesList = file.readlines()  
  # CurrGenPop holds population/list of randomly generated chromosomes.
  currGenPop = [initialize_chromosome() for _ in range(parameterDictionary["PopulationSize"])]
  # Loop iterations dependent on number of generations
  generationNum = 0 # generation counter
  for _ in range(parameterDictionary["numGenerations"]):
    # nextGenPop stores the next generation
    nextGenPop = createNextGen(currGenPop, linesList)
    generationNum += 1
    # Move to the next generation, for next iteration.
    currGenPop = nextGenPop[:] 
    # Calculate fitness statistics for every 10th generation
    if generationNum != 0 and generationNum % 10 == 0: # Keeping track of every 10 gens.
      calculatefitnessStats(currGenPop, generationNum, linesList)
    # ensure loop exit for correct num of gens. 
    if (generationNum == parameterDictionary["numGenerations"]): 
      break
  # Find and display highest fitness chromosome from the final generation.   
  displayHighestFitness(currGenPop, linesList)

main()