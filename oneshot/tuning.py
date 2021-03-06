import sys
sys.path.append('../') # <- uncomment this if you don't have simulator in your path
from multishot import MultiShot
from simulator import queue_simulator, run_queue
import numpy as np

min_over = 100
max_revenue = 0

range_step = 10

# Set parameters here

lambda_h_min = 0.05
lambda_h_max = 0.2
range_h_min = int(lambda_h_min * 100)
range_h_max = int(lambda_h_max * 100)

lambda_e_min = 0.6
lambda_e_max = 0.8
range_e_min = int(lambda_e_min * 100)
range_e_max = int(lambda_e_max * 100)

lambda_l_min = 0.7
lambda_l_max = 1.0
range_l_min = int(lambda_l_min * 100)
range_l_max = int(lambda_l_max * 100)

bucket_min = 60
bucket_max = 100

# Run simulator on the queued algorithms

for h in range(range_h_min, range_h_max, range_step):
    for e in range(range_e_min, range_e_max, range_step):
        for l in range(range_l_min, range_l_max, range_step):
            for i in range(bucket_min, bucket_max, 10):
                print("h: " + str(0.01 * h), " e: " + str(0.01 * e) + " l: " + str(0.01 * l) + " bucket(s): " + str(i))
                oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.01 * h, 'lamb_e': 0.01 * e, 'lamb_l': 0.01 * l, 'time': 0}
                oneshot = MultiShot(i, oneshot_args=oneshot_args, limit=3)
                queue_simulator(oneshot, "Multishot (%d bucket(s)): (h=%.2f, e=%.2f, l=%.2f)" % (i, 0.01 * h, 0.01 * e, 0.01 * l))

results = run_queue(limit=1)  # <- take away the 'none' too print stats

# Find parameters with the best revenue, lowest overshoot

index = 0
for h in range(range_h_min, range_h_max, range_step):
    for e in range(range_e_min, range_e_max, range_step):
        for l in range(range_l_min, range_l_max, range_step):
            for i in range(bucket_min, bucket_max, 10):
                stats = results[index][1].stats
                over_percent = 100 * stats.price_floor_too_high_count / stats.auction_count_non_null
                revenue = stats.total_revenue
                if over_percent < min_over:
                    min_over = over_percent
                    over_hyper_h = 0.01 * h
                    over_hyper_e = 0.01 * e
                    over_hyper_l = 0.01 * l
                    over_bucket = i
                if revenue > max_revenue:
                    max_revenue = revenue
                    revenue_hyper_h = 0.01 * h
                    revenue_hyper_e = 0.01 * e
                    revenue_hyper_l = 0.01 * l
                    revenue_bucket = i
                index += 1


print("overshooting best h: %f best e: %f best l: %f best bucket(s): %d" % (over_hyper_h, over_hyper_e, over_hyper_l, over_bucket))
print("revenue best h: %f best e: %f best l: %f best bucket(s): %d" % (revenue_hyper_h, revenue_hyper_e, revenue_hyper_l, revenue_bucket))
