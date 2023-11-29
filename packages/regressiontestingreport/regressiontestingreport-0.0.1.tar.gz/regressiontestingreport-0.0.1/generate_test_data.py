import random
import pandas as pd
import math

# max_steps = 900
# current_step = 0

# while len(d["success-rate"]) < 1000:
#     if random.random() * max_steps > max_steps - current_step:
#         decay_factor = math.exp(-current_step / max_steps)
#     else:
#         decay_factor = math.exp(-current_step / max_steps) * 2  # Increase the decay factor for faster decrease
#     current_step += 1

#     j = max(0, 100 * decay_factor)
#     while len(d["success-rate"]) < 1000 and j >= 0:
#         d["success-rate"].append(j)
#         decay_factor *= 0.95  # Adjust the decay factor here for the rate of exponential decrease

def generate_data():
     d = {}
     d["success-rate"] = [100] * 200
     num_points = 800

     # Generate the list using the decay factor
     for i in range(200, num_points+200):
          d["success-rate"].append(100 - (100/(800 ** 2))*((i-200)**2) + random.uniform(-0.3, 0.3))
     


     d["reward"] = [random.random() for i in range(1000)]
     d["collision-rate"] = [random.random() for i in range(1000)]

     df = pd.DataFrame(data = d)
     df.to_csv('fake-data.csv', index=False)

