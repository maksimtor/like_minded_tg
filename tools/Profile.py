from geopy.distance import geodesic

class UserInfo:
	def __init__(self, data):
		self.name = data["name"]
		self.description = data.get("description", None)
		self.interests = data.get("interests", [])
		self.music = data.get("music", [])
		self.pol_coords = data.get("pol_coords", None)
		self.geo_coords = data.get("geo_coords", None)
		self.age = data.get("age", None)
		self.gender = data.get("gender", None)
		self.personality = data.get("personality", None)

class UserPrefs:
	def __init__(self, data):
		self.age_pref = data.get("age_pref", (18, 100, 25))
		self.area_restrict = data.get("area_restrict", 20000)
		self.goal = data.get("goal", None)
		self.gender_pref = data.get("gender_pref", None)
		self.pol_pref = data.get("pol_pref", True)
		self.int_pref = data.get("int_pref", True)
		self.music_pref = data.get("music_pref", True)
		self.loc_pref = data.get("loc_pref", True)
		self.pers_pref = data.get("pers_pref", True)

class Profile:
	def __init__(self, data=None):
		if data:
			self.set_profile(data)
	
	def set_profile(self, data):
		self.profile_id = data.get('profile_id', None)
		self.tg_id = data.get('tg_id', 'to')
		self.active = data.get("active", True)
		if "user_info" in data and "user_prefs" in data:
			self.user_info = UserInfo(data["user_info"])
			self.user_prefs = UserPrefs(data["user_prefs"])
		else:
			self.user_info = UserInfo(data)
			self.user_prefs = UserPrefs(data)
		self.photo = data.get("photo", None)

	def __repr__(self):
		return str(self.user_info.geo_coords)

	def get_profile(self):
		return {
			"tg_id": self.tg_id,
			"active": self.active,
			"user_info": {
				"name": self.user_info.name,
				"description": self.user_info.description,
				"interests": self.user_info.interests,
				"music": self.user_info.music,
				"pol_coords": self.user_info.pol_coords,
				"geo_coords": self.user_info.geo_coords,
				"age": self.user_info.age,
				"gender": self.user_info.gender,
				"personality": self.user_info.personality
			},
			"user_prefs": {
				"age_pref": self.user_prefs.age_pref,
				"area_restrict": self.user_prefs.area_restrict,
				"goal": self.user_prefs.goal,
				"gender_pref": self.user_prefs.gender_pref,
				"pol_pref": self.user_prefs.pol_pref,
				"int_pref": self.user_prefs.int_pref,
				"music_pref": self.user_prefs.music_pref,
				"loc_pref": self.user_prefs.loc_pref,
				"pers_pref": self.user_prefs.pers_pref,
			},
			"photo": self.photo
		}

	def public_data(self, main_profile_coords = (0, 0)):
		return {
			"name": self.user_info.name,
			"distance": geodesic(self.user_info.geo_coords, main_profile_coords).km,
			"description": self.user_info.description,
			"interests": self.user_info.interests,
			"music": self.user_info.music,
			"age": self.user_info.age,
			"gender": self.user_info.gender,
			"photo": self.photo
		}
