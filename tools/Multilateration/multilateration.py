# -*- coding: utf-8 -*-
import math

from scipy.optimize import minimize


##################### Codigo de multilateração de dados obtidos durante o voo #############################


# https://www.alanzucconi.com/2017/03/13/understanding-geographical-coordinates/
# https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/

# locations: [ (lat1, long1), ... ]
# distances: [ distance1,     ... ]   Em kilômetros

class multilateration(object):

	def __init__(self, locations, distances):

		data = zip(distances,locations)
#		print len(data)
#		print data

		# Initial point: o ponto mais próximo ao alvo
		min_distance = float('inf')
		closest_location = None

		# Faz uma busca na matriz de distância pelo ponto de coleta mais próximo ao alvo
		for n in range(len(distances)):
			if distances[n] < min_distance:
				min_distance = distances[n]
				print "A nova distância mínima a ser adotada como inicial será: {}".format(min_distance)
				closest_location = locations[n]
				print  "A localização inicial adotada será: {}".format(closest_location)
				initial_location = closest_location

		result = minimize(
			self.mse,  						# Chama o método de cálculo de erro
			initial_location,  				# Chute inicial
			args=(locations, distances),  	# Additional parameters for mse
			method='L-BFGS-B',  			# Algoritmo de otmizaçãom
			options={
				'ftol': 1e-5,  				# Tolerância
				'maxiter': 1e+7  			# número máximo de interações
			})
		location = result.x
		print result
		print location

#	Cálculo de distâncias entre coordenadas geográficas:
	def geographical_distance(self, latitudeA, longitudeA, latitudeB, longitudeB):
		# Conversão de graus para radianos
		delta_latitude = math.radians(latitudeB - latitudeA)
		delta_longitude = math.radians(longitudeB - longitudeA)
		mean_latitude = math.radians((latitudeA + latitudeB) / 2.0)

		R = 6371.009  # Km

		# Planificação da superfície esférica da Terra
		return R * math.sqrt(math.pow(delta_latitude,2) + math.pow(math.cos(mean_latitude) * delta_longitude,2))

#	Cálculo de interseção de circunferências:
	def great_circle_distance (self, latitudeA, longitudeA, latitudeB, longitudeB):
		# Conversão de graus para radianos
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

# 	Método de Mean Square Error (Erro quadrático médio ou risco quadrático)
#	https://en.wikipedia.org/wiki/Mean_squared_error

	def mse(self, x, locations, distances):
		data = zip(distances, locations)
		mse = 0.0
		for location, distance in zip(locations, distances):
			distance_calculated = self.great_circle_distance(x[0], x[1], location[0], location[1])
			mse += math.pow(distance_calculated - distance, 2.0)
		print mse
		return mse / len(data)





