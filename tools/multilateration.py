import math
import scipy
import numpy

# https://www.alanzucconi.com/2017/03/13/understanding-geographical-coordinates/
# https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/
# Mean Square Error
from scipy.optimize import minimize

locations = [(-22.86985120,-43.1051227),(-22.86983310,-43.1051285),(-22.86984080,-43.1051355),(-22.86983130,-43.1051311),(-22.86984440,-43.1051408),(-22.86987940,-43.1051325),(-22.86986800,-43.1051353),(-22.86986740,-43.1051099),(-22.86982530,-43.1051313),(-22.86986990,-43.1051268),(-22.86987800,-43.1051076),(-22.86984740,-43.1051061),(-22.86984480,-43.1051351),(-22.86984460,-43.1051185),(-22.86986010,-43.1051341),(-22.86987300,-43.1051315),(-22.86985720,-43.1051022),(-22.86986560,-43.1051251),(-22.86986950,-43.1051279),(-22.86987230,-43.1051344),(-22.86984940,-43.1051007),(-22.86984500,-43.1051201),(-22.86992110,-43.1050613),(-22.86984650,-43.1050980),(-22.86997450,-43.1050409),(-22.86984980,-43.1050972),(-22.86989680,-43.1050272),(-22.86984260,-43.1050673),(-22.86982940,-43.1050112),(-22.86996080,-43.1050254)]
distances = (0.000251189,0.000271227,0.000292864,0.000316228,0.000316228,0.000398107,0.000398107,0.000398107,0.000398107,0.000429866,0.000429866,0.000464159,0.000464159,0.000501187,0.000681292,0.000735642,0.000926119,0.001000000,0.001079775,0.001165914,0.001165914,0.001847850,0.001847850,0.002712273,0.002712273,0.002928645,0.002928645,0.003162278,0.003981072,0.005843414)
data = zip(distances,locations)
print len(data)


# Initial point: the point with the closest distance
min_distance = float('inf')
closest_location = None

# A new closest point!
for n in range(len(distances)):
    if distances[n] < min_distance:
        min_distance = distances[n]
        print min_distance
        closest_location = locations[n]
        print  closest_location
        initial_location = closest_location


def geographical_distance(latitudeA, longitudeA, latitudeB, longitudeB):
    # Degrees to radians
    delta_latitude = math.radians(latitudeB - latitudeA)
    delta_longitude = math.radians(longitudeB - longitudeA)
    mean_latitude = math.radians((latitudeA + latitudeB) / 2.0)

    R = 6371.009  # Km

    # Spherical Earth projected to a plane
    return \
        R * math.sqrt \
                (
                math.pow
                    (
                    delta_latitude,
                    2
                )
                +
                math.pow
                    (
                    math.cos(mean_latitude) *
                    delta_longitude,
                    2
                )
            )

def great_circle_distance (latitudeA, longitudeA, latitudeB, longitudeB):
	# Degrees to radians
	phi1    = math.radians(latitudeA)
	lambda1 = math.radians(longitudeA)

	phi2    = math.radians(latitudeB)
	lambda2 = math.radians(longitudeB)

	delta_lambda = math.fabs(lambda2 - lambda1)

	central_angle = \
		math.atan2 \
		(
			# Numerator
			math.sqrt
			(
				# First
				math.pow
				(
					math.cos(phi2) * math.sin(delta_lambda)
					, 2.0
				)
				+
				# Second
				math.pow
				(
					math.cos(phi1) * math.sin(phi2) -
					math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
					, 2.0
				)
			),
			# Denominator
			(
				math.sin (phi1) * math.sin(phi2) +
				math.cos (phi1) * math.cos(phi2) * math.cos(delta_lambda)
			)
		)

	R = 6371.009 # Km
	return R * central_angle

def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1])
        mse += math.pow(distance_calculated - distance, 2.0)
    print mse
    return mse / len(data)


# locations: [ (lat1, long1), ... ]
# distances: [ distance1,     ... ]
result = minimize(
	mse,                         # The error function
	initial_location,            # The initial guess
	args=(locations, distances), # Additional parameters for mse
	method='L-BFGS-B',           # The optimisation algorithm
	options={
		'ftol':1e-5,         # Tolerance
		'maxiter': 1e+7      # Maximum iterations
	})
location = result.x
print location
print result


