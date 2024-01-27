# Genetic Algorithm for Financial Data Analysis

## Overview:

This Python program implements a Genetic Algorithm to analyze financial data for 2-day chart patterns. It evolves a population of chromosomes to find the most profitable patterns within the data. The user has the option to configure various parameters and appropriately analyze the financial data.

## Parameter description and Valid input instructions:

The program provides several parameters that you can customize for your analysis. Here's an explanation of each parameter:

- "fileName": The name of the file containing the training data. This file should contain financial data with each line representing a data point.
- Input: Correct filename that is present in the IDE file system. Filename is case sensitive, thus input must exactly match the file name. File name should be followed by correct file extension(.txt). Example: Debugging.txt

- "PopulationSize": The number of chromosomes in each generation. This parameter controls the size of the population that the algorithm evolves.
- Input: Must be a positive integer value. Example: Correct = {1,5,100...} Incorrect = {0, negative int, strings}

- "numGenerations": The number of generations the algorithm should run. This parameter determines how many generations the algorithm will evolve.
- Input: Must be a positive integer value. Example: Correct = {1,5,100...} Incorrect = {0, negative int, strings}

- "X_Percent": Elitism rate or the percentage of chromosomes to be cloned without changes. It controls the percentage of the best-performing chromosomes in each generation that are copied to the next generation without modification.
- Input: Range 0 - 30

- "crossoverAlgorithm": Type of crossover algorithm. It can be set to "uniform" or "1-point" to specify the type of crossover used in the algorithm.
- Input: Type either "uniform" or "1-point". Not case sensitive, therefore "UNIform" "1-POiNt" are also valid.

- "Z_Percent": Mutation rate or the probability of gene mutation, expressed as a percentage. This parameter controls how often genes in a chromosome will be mutated.
- Input: Range 0 - 30


## Usage of Genetic Algorithm for financial data analysis:

- Steps:

1. Ensure you have a file containing the financial data you want to analyze. Make sure the file is in the correct format, with each line representing a data point.

2. Run the program and provide the required parameters as prompted.

3. The algorithm will generate and evolve a population of chromosomes over the specified number of generations.

4. At the end of the algorithm's execution, it will display the highest fitness chromosome from the final generation, along with its fitness score.


## Parameter combination for best performance: 


PopulationSize: 80
numGenerations: 150
X_Percent: 25
crossoverAlgorithm: uniform
Z_Percent: 5


# fileName: Debugging.txt
*****************************
Statistics After: Generation 150
Max Fitness: 31.5
Min Fitness: -4.48
Average Fitness (Mean): 26.01
Median Fitness: 31.5
*****************************

Highest Fitness Chromosome from the Final Generation:
Chromosome: [-1.07, 0.17, -0.57, 0.1, 1.0]
Fitness Score: 31.5


# fileName: genAlgData1.txt
*****************************
Statistics After: Generation 150
Max Fitness: 5194.12
Min Fitness: 3.85
Average Fitness (Mean): 4446.85
Median Fitness: 5194.12
*****************************

Highest Fitness Chromosome from the Final Generation:
Chromosome: [-0.78, 1.14, -2.25, 1.55, 0.0]
Fitness Score: 5194.12


# fileName: genAlgData2.txt
*****************************
Statistics After: Generation 150
Max Fitness: 460.03
Min Fitness: -277.01
Average Fitness (Mean): 370.35
Median Fitness: 460.03
*****************************

Highest Fitness Chromosome from the Final Generation:
Chromosome: [-3.79, 1.5, -2.98, 0.35, 0.0]
Fitness Score: 460.03
