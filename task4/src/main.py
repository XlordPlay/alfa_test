import pulp
import pandas as pd
import matplotlib.pyplot as plt
class Factory:
    def __init__(self, id, x, y, supply):
        self.id = id
        self.x = x
        self.y = y
        self.supply = supply

class Shop:
    def __init__(self, id, x, y, demand):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand

class OptimizationModel:
    def __init__(self, factories, shops):
        """
            factories, stores: Lists of factories and stores passed in when creating the model.
            
            model: Create an optimization model that will maximize profit.
            
            transport_vars: A dictionary to store variables representing the amount of candy transported from factories to stores.
            
            open_shop_vars: A dictionary to store variables representing whether stores are open or closed.
        """
        self.factories = factories
        self.shops = shops
        self.model = pulp.LpProblem("Candy_Optimization", pulp.LpMaximize)
        self.transport_vars = {}
        self.open_shop_vars = {}

    def setup_variables(self):
        """

            This function creates variables for each possible transportation link between factories and stores.
            Each variable specifies how many candies will be delivered.
            Also creates binary variables for the stores that indicate whether they are open (1) or closed (0).

        """
        for i, factory in enumerate(self.factories):
            for j, shop in enumerate(self.shops):
                self.transport_vars[(i, j)] = pulp.LpVariable(f"Transport_{factory.id}_{shop.id}", lowBound=0)
        self.open_shop_vars = pulp.LpVariable.dicts("OpenShop", range(len(self.shops)), cat='Binary')

    def setup_objective(self):
        """

            Identifies the target function that maximizes profit:
                Revenue from candy sales
                Fixed costs of open stores are subtracted
                Production and shipping costs are subtracted

            All this information is summarized and added to the model

        """
        profit = pulp.lpSum(
        (
            800 * self.transport_vars[i, j]  #Sales revenue
            - 200 * self.transport_vars[i, j]  #Cost price
            - 20 * ((self.factories[i].x - shop.x)**2 + (self.factories[i].y - shop.y)**2)**0.5 * self.transport_vars[i, j]  #Delivery
        )
        for i, factory in enumerate(self.factories)
        for j, shop in enumerate(self.shops)
            ) - pulp.lpSum(10000 * self.open_shop_vars[j] for j in range(len(self.shops)))  #Shop rent

        self.model += profit

    def setup_constraints(self):

        """
            Sets limits on the model:

                The total amount of candy delivered from a factory must not exceed its production capacity

                The total amount of candy received by each store must not exceed its demand multiplied by a 
                binary variable indicating whether the store is open

        """
        #Restrictions on production
        for i, factory in enumerate(self.factories):
            self.model += pulp.lpSum(self.transport_vars[i, j] for j in range(len(self.shops))) <= factory.supply

        #Demand constraints
        for j, shop in enumerate(self.shops):
            self.model += pulp.lpSum(self.transport_vars[i, j] for i in range(len(self.factories))) <= shop.demand
            self.model += pulp.lpSum(self.transport_vars[i, j] for i in range(len(self.factories))) <= shop.demand * self.open_shop_vars[j]



    def solve(self):
        """
            Invokes methods to set the variables, target function,
            and constraints, and then solves the model.
        """
        self.setup_variables()
        self.setup_objective()
        self.setup_constraints()
        self.model.solve()

    def get_results(self):
        """
            Gets total returns and creates a dictionary to store the results
        """
        total_profit = pulp.value(self.model.objective)
        results = {
            "Total Profit": total_profit,
            "Transport": {},
            "Closed Shops": [],
            "Unallocated Candies": [],
            "Unmet Demand": [],
            "Profitability": {}
        }

        """
            collecting data on transportation, closed stores,
            unallocated candy, and profitability of open stores.

        """
        for i in range(len(self.factories)):
            for j in range(len(self.shops)):
                if self.transport_vars[i, j].varValue > 0:
                    results["Transport"][(self.factories[i].id, self.shops[j].id)] = self.transport_vars[i, j].varValue

        for j in range(len(self.shops)):
            if self.open_shop_vars[j].varValue == 0:
                results["Closed Shops"].append(self.shops[j].id)

            unmet_demand = self.shops[j].demand - pulp.value(pulp.lpSum(self.transport_vars[i, j] for i in range(len(self.factories))))
            results["Unmet Demand"].append(unmet_demand)

            if self.open_shop_vars[j].varValue == 1:
                profit_for_shop = (
                    800 * pulp.value(pulp.lpSum(self.transport_vars[i, j] for i in range(len(self.factories))))  #Revenue
                    - 200 * pulp.value(pulp.lpSum(self.transport_vars[i, j] for i in range(len(self.factories))))  #Production
                    - pulp.lpSum(20 * ((self.factories[i].x - self.shops[j].x)**2 + (self.factories[i].y - self.shops[j].y)**2)**0.5 * self.transport_vars[i, j] for i in range(len(self.factories)))  #Delivery
                    - 10000  #rent
                )

                
                results["Profitability"][self.shops[j].id] = profit_for_shop

        for i in range(len(self.factories)):
            unsold_candies = self.factories[i].supply - pulp.value(pulp.lpSum(self.transport_vars[i, j] for j in range(len(self.shops))))
            results["Unallocated Candies"].append(unsold_candies)

        return results
    
    def visualize_results(self, results):
    
        transport_data = results["Transport"]
        transport_values = list(transport_data.values())
        transport_labels = [f"{key[0]} to {key[1]}" for key in transport_data.keys()]

        plt.figure(figsize=(12, 6))
        plt.bar(transport_labels, transport_values, color='skyblue')
        plt.xticks(rotation=45)
        plt.title('Transport Volume from Factories to Shops')
        plt.xlabel('Transport Routes')
        plt.ylabel('Volume of Candies')
        plt.tight_layout()
        

        profitability_data = results["Profitability"]
        shop_labels = list(profitability_data.keys())
        shop_profits = list(profitability_data.values())

        plt.figure(figsize=(12, 6))
        shop_profits = [pulp.value(profit) for profit in shop_profits]
        plt.bar(shop_labels, shop_profits, color='lightgreen')
        plt.xticks(rotation=45)
        plt.title('Profitability of Open Shops')
        plt.xlabel('Shops')
        plt.ylabel('Profit')
        plt.tight_layout()
        plt.show()


factories_data = pd.read_csv('/home/xlordplay/alfa_test_tasks/alfa_test/data/Input data/fact.dat', sep=';', names=['id', 'x', 'y', 'supply'], header=0)
shops_data = pd.read_csv('/home/xlordplay/alfa_test_tasks/alfa_test/data/Input data/shop.dat', sep=';', names=['id', 'x', 'y', 'demand'], header=0)


factories = [Factory(row['id'], row['x'], row['y'], row['supply']) for _, row in factories_data.iterrows()]
shops = [Shop(row['id'], row['x'], row['y'], row['demand']) for _, row in shops_data.iterrows()]


model = OptimizationModel(factories, shops)
model.solve()


results = model.get_results()

print("=" * 50)
print("Candy Distribution Optimization Results")
print("=" * 50)
print(f"Total Profit: {results['Total Profit']:.2f} currency units")


print("\nTransport Volume:")
for (factory_id, shop_id), volume in results['Transport'].items():
    print(f" - {factory_id} -> {shop_id}: {volume:.1f} candies")

print("\nClosed Shops:")
if results['Closed Shops']:
    print(" - " + ", ".join(results['Closed Shops']))
else:
    print(" - No closed shops")

print("\nUnallocated Candies by Factory:")
for i, unallocated in enumerate(results['Unallocated Candies']):
    print(f" - Factory {factories[i].id}: {unallocated:.1f} candies")

print("\nUnmet Demand by Shop:")
for j, unmet in enumerate(results['Unmet Demand']):
    print(f" - Shop {shops[j].id}: {unmet:.1f} candies")

print("\nProfitability of Open Shops:")
for shop_id, profit in results['Profitability'].items():
    print(f" - {shop_id}: {pulp.value(profit)} currency units")

print("=" * 50)


model.visualize_results(results)
