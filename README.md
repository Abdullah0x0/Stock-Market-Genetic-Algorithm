# Genetic Algorithm for Financial Data Analysis

This Python application leverages a Genetic Algorithm (GA) to analyze and identify profitable 2-day chart patterns within financial data. It is designed to evolve a population of chromosomes (potential solutions) through generations to optimize the identification of profitable trading strategies.

## Overview

The program allows users to input financial data and set various parameters to tailor the genetic algorithm's operation. By evolving chromosomes across generations, the algorithm aims to discover the most effective combinations that represent profitable chart patterns in the provided financial data.

## Features

- **Customizable Parameters**: Adjust population size, number of generations, elitism rate, crossover algorithm type, and mutation rate to fine-tune the analysis.
- **Support for Various Data Files**: Analyze different financial datasets by specifying the file name containing the training data.
- **Dynamic Genetic Operations**: Choose between "uniform" and "1-point" crossover algorithms to influence how new generations are created.
- **Performance Statistics**: Track the performance of the algorithm with statistics like maximum, minimum, average, and median fitness scores.

## Getting Started

### Requirements

- Python 3.x
- NumPy library

### Installation

1. Ensure Python 3.x is installed on your system. Download it from [python.org](https://www.python.org/) if necessary.
2. Install NumPy using pip:
   ```
   pip install numpy
   ```

### Configuration and Usage

1. Clone this repository or download `Stock Market Genetic Algorithm.py` to your local machine.
2. Prepare your financial data in a text file, with each line representing a data point.
3. Run the program:
   ```
   python "Stock Market Genetic Algorithm.py"
   ```
4. When prompted, input the parameters as follows:
   - `fileName`: The path to your data file.
   - `PopulationSize`: A positive integer indicating the number of chromosomes per generation.
   - `numGenerations`: A positive integer specifying the number of generations to evolve.
   - `X_Percent`: The elitism rate (0-30), determining the percentage of top chromosomes carried over to the next generation without changes.
   - `crossoverAlgorithm`: Type "uniform" or "1-point" to set the crossover algorithm.
   - `Z_Percent`: The mutation rate (0-30), indicating the percentage chance of gene mutation within a chromosome.

## Parameter Recommendations

For optimal performance, consider starting with the following settings:
- `PopulationSize`: 80
- `numGenerations`: 150
- `X_Percent`: 25
- `crossoverAlgorithm`: "uniform"
- `Z_Percent`: 5

Adjust these parameters based on your dataset and analysis needs.
