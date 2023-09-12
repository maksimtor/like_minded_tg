from math import sqrt
from geopy.distance import geodesic

def flatten(t):
	return [item for sublist in t for item in sublist]

class LikenessCalculator:
	def __init__(self, main_user, target_user):
		self.main_info = main_user.user_info
		self.prefs = main_user.user_prefs
		self.target_data = target_user.user_info
		self.score = 0
		self.uni_weight = self.calc_uni_weight()

	def calc_uni_weight(self):
		uni_weight = 0
		if self.prefs.pol_pref == True:
			uni_weight += 1

		if self.prefs.loc_pref == True:
			uni_weight += 1

		if self.prefs.int_pref == True:
			uni_weight += 1

		if self.prefs.music_pref == True:
			uni_weight += 1

		if self.prefs.age_pref:
			uni_weight += 1

		if self.prefs.pers_pref == True:
			uni_weight += 1

		return (10/uni_weight)/10

	def calc_polit_likeness(self):
		if self.prefs.pol_pref == True:
			if self.target_data.pol_coords == None:
				return 0.4
			else:
				dist = sqrt( (self.target_data.pol_coords[0]/10 - self.main_info.pol_coords[0]/10)**2 + (self.target_data.pol_coords[1]/10 - self.main_info.pol_coords[1]/10)**2 )
				return 1-dist/2.8284271247461903
		else:
			return 0

	def calc_location_likeness(self):
		if self.prefs.loc_pref == True:
			if self.target_data.geo_coords == None:
				return 0.4
			else:
				# approximate radius of earth in km
				distance = geodesic(self.target_data.geo_coords, self.main_info.geo_coords).km,
				if distance[0]<2000:
					res = 1 - distance[0]/2000
				else:
					res = 0
				return (res ** 3)
		else:
			return 0

	def calc_intererests_likeness(self):
		if self.prefs.int_pref == True:
			if self.target_data.interests == None or self.target_data.interests == []:
				return 0.4
			else:
				l = len(self.main_info.interests)
				a = flatten(self.main_info.interests)
				b = flatten(self.target_data.interests)
				common_elements = list(set(self.main_info.interests).intersection(self.target_data.interests))
				return len(common_elements)/l
		else:
			return 0

	def calc_music_likeness(self):
		if self.prefs.music_pref == True:
			if self.target_data.music == None or self.target_data.music == []:
				return 0.4
			else:
				l = len(self.main_info.music)
				a = flatten(self.main_info.music)
				b = flatten(self.target_data.music)
				common_elements = list(set(self.main_info.music).intersection(self.target_data.music))
				return len(common_elements)/l
		else:
			return 0

	def calc_age_likeness(self):
		if self.prefs.age_pref:
			if self.target_data.age == None:
				return 0.4
			else:
				optimal_age = int(self.prefs.age_pref[2])
				min_age = int(self.prefs.age_pref[0])
				max_age = int(self.prefs.age_pref[1])

				targetAge = int(self.target_data.age)

				max_dist = max(optimal_age-min_age, max_age-optimal_age)+5
				act_dist = abs(targetAge-optimal_age)
				return 1-(act_dist/max_dist)**2
		else:
			return 0

	def calc_personality_likeness(self):
		if self.prefs.pers_pref:
			if self.target_data.personality == None:
				return 0.4
			else:
				result = 0
				# scoring extraversion
				main_points = self.main_info.personality[0]
				target_points = self.target_data.personality[0]
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring agreeableness
				main_points = self.main_info.personality[1]
				target_points = self.target_data.personality[1]
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring openness
				main_points = self.main_info.personality[2]
				target_points = self.target_data.personality[2]
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring conscientiousness
				main_points = self.main_info.personality[3]
				target_points = self.target_data.personality[3]
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2

				# scoring neuroticism
				main_points = self.main_info.personality[4]
				target_points = self.target_data.personality[4]
				max_dist = max(1-main_points, main_points)
				act_dist = abs(target_points-main_points)
				r_score = 1-(act_dist/max_dist)
				result+=r_score*0.2
				return result
		else:
			return 0

	def calc_likeness(self):
		return self.uni_weight*(self.calc_polit_likeness() + self.calc_location_likeness() + self.calc_intererests_likeness() + + self.calc_music_likeness() + self.calc_age_likeness() + self.calc_personality_likeness())


class ProfileCalculations:
	def __init__(self, profile, potential_profiles):
		self.profile = profile
		self.potential_profiles = potential_profiles

	def calculate_likeness(self, potential_profile):
		likeness_calculator = LikenessCalculator(self.profile, potential_profile)
		return likeness_calculator.calc_likeness()

	def sort_by_likeness(self):
		for profile in self.potential_profiles:
			profile.likeness = self.calculate_likeness(profile)
		self.potential_profiles.sort(key=lambda x: x.likeness, reverse=True)
		return self.potential_profiles
