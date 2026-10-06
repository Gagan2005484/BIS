import numpy as np

# 1. Define the Agricultural Cost/Fitness Function
def evaluate_coverage(particle, target_coverage):
    """
    Calculates the error between the current particle position (sensor allocation)
    and the ideal target coverage inputs from the user. Lower error = better fitness.
    """
    return float(np.sum((particle - target_coverage) ** 2))

# 2. Main Particle Swarm Optimization Algorithm
def run_agriculture_pso(target_coverage, num_particles=20, max_iterations=50):
    dim = len(target_coverage)
    
    # Initialize particle positions randomly between 0 and 100% sensor capacity
    X = np.random.uniform(0, 100, (num_particles, dim))
    # Initialize velocities to zero
    V = np.zeros((num_particles, dim))
    
    # Track personal best configurations
    pbest = X.copy()
    pbest_fitness = np.array([evaluate_coverage(p, target_coverage) for p in X])
    
    # Track global best configuration
    gbest_index = np.argmin(pbest_fitness)
    gbest = pbest[gbest_index].copy()
    gbest_fitness = pbest_fitness[gbest_index]
    
    # PSO Hyperparameters
    w = 0.5   # Inertia weight
    c1 = 1.5  # Cognitive coefficient (pull toward personal best)
    c2 = 1.5  # Social coefficient (pull toward global best)
    
    # Optimization Loop
    for _ in range(max_iterations):
        for i in range(num_particles):
            # Generate random coefficients
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            
            # Apply the Velocity Update Formula
            V[i] = (w * V[i] + 
                    c1 * r1 * (pbest[i] - X[i]) + 
                    c2 * r2 * (gbest - X[i]))
            
            # Update Position
            X[i] = X[i] + V[i]
            
            # Keep allocation values within valid bounds [0% to 100%]
            X[i] = np.clip(X[i], 0, 100)
            
            # Evaluate new position
            current_fitness = evaluate_coverage(X[i], target_coverage)
            
            # Update Personal Best if improved
            if current_fitness < pbest_fitness[i]:
                pbest_fitness[i] = current_fitness
                pbest[i] = X[i].copy()
                
            # Update Global Best if improved
            if current_fitness < gbest_fitness:
                gbest_fitness = current_fitness
                gbest = X[i].copy()
                
    return gbest, gbest_fitness

# 3. Interactive User Interface
if __name__ == "__main__":
    print("=== Agriculture Monitoring PSO Optimizer ===")
    print("Enter the ideal sensor deployment coverage levels (%) for your farm zones.")
    
    try:
        zone_a = float(input("Ideal allocation for Zone A (0-100%): "))
        zone_b = float(input("Ideal allocation for Zone B (0-100%): "))
        zone_c = float(input("Ideal allocation for Zone C (0-100%): "))
        
        user_targets = np.array([zone_a, zone_b, zone_c])
        
        print("\nOptimizing deployment strategy using Swarm Intelligence...")
        best_allocation, minimum_error = run_agriculture_pso(user_targets)
        
        print("\n=== Optimization Results ===")
        print(f"Optimal Allocation for Zone A: {best_allocation[0]:.2f}%")
        print(f"Optimal Allocation for Zone B: {best_allocation[1]:.2f}%")
        print(f"Optimal Allocation for Zone C: {best_allocation[2]:.2f}%")
        print(f"Final Optimization Error Margin: {minimum_error:.6f}")
        
    except ValueError:
        print("Please enter valid numeric values for the percentages.")





=== Agriculture Monitoring PSO Optimizer ===
Enter the ideal sensor deployment coverage levels (%) for your farm zones.
Ideal allocation for Zone A (0-100%): 85.5
Ideal allocation for Zone B (0-100%): 40.2
Ideal allocation for Zone C (0-100%): 75.0

Optimizing deployment strategy using Swarm Intelligence...

=== Optimization Results ===
Optimal Allocation for Zone A: 85.50%
Optimal Allocation for Zone B: 40.20%
Optimal Allocation for Zone C: 75.00%
Final Optimization Error Margin: 0.000000


v
