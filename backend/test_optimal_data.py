import pandas as pd
from services.ga import run_ga, fitness

# Test with optimal sample data
print('Testing GA with optimal data format...')
df = pd.read_csv('../sample_optimal_timetable.csv')
print(f'Dataset: {len(df)} courses')
print(f'Unique lecturers: {df["lecturer"].nunique()}')
print(f'Unique groups: {df["group"].nunique()}')
print(f'Unique rooms: {df["room"].nunique()}')
print(f'Average class size: {df["students"].mean():.1f} students')
print(f'Capacity utilization: {(df["students"] / df["capacity"]).mean():.1%}')

print('\nRunning GA...')
result = run_ga(df)
final_fitness = fitness(result)
print(f'Final fitness: {final_fitness}')
print('GA completed successfully!')