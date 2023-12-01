import time

from src.sumo_experiments import Experiment
from src.sumo_experiments.preset_networks import GridNetwork
from src.sumo_experiments.traci_util import *
from src.sumo_experiments.strategies import *

net = GridNetwork(5, 5)
infrastructures = net.generate_infrastructures(200, 30, 3, 50)
flows = net.generate_flows_all_directions(1800, 300)
detectors = net.generate_numerical_detectors()

exp = Experiment(
    name='test',
    infrastructures=infrastructures,
    flows=flows,
    detectors=detectors
)

min_phases_duration = {f'x{x}-y{y}': [10, 10] for y in range(6) for x in range(6)}
max_phases_duration = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
yellow_times = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
thresholds = {f'x{x}-y{y}': 5 for y in range(6) for x in range(6)}
#min_phases_duration = {f'c': [10, 10]}
#max_phases_duration = {f'c': None}
#thresholds = {f'c': 5}
counted_vehicles = 'stopped'
#phases_duration = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
#yellow_times = {'c': 3}
#yellow_times = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
strategy = NumericalStrategy(infrastructures,
                             detectors,
                             min_phases_durations=min_phases_duration,
                             max_phases_durations=max_phases_duration,
                             counted_vehicles=counted_vehicles,
                             thresholds=thresholds,
                             yellow_times=yellow_times)

tw = TraciWrapper(1800)
tw.add_stats_function(get_co2_emissions_data)
tw.add_behavioural_function(strategy.run_all_agents)

t = time.time()

#data = exp.run_traci(tw.final_function, nb_threads=8)
data = exp.run_traci(tw.final_function, gui=True, no_warnings=True, nb_threads=8)

exp.clean_files()

print(time.time() - t)




