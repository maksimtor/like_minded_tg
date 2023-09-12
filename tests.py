import unittest
import copy
import time
from tools import Profile, ProfileCalculations, ProfileDb, app_data
from functools import wraps

def timeit(func):
	@wraps(func)
	def timeit_wrapper(*args, **kwargs):
		res = 0
		for i in range(100):
			start_time = time.perf_counter()
			result = func(*args, **kwargs)
			end_time = time.perf_counter()
			total_time = (end_time - start_time)*1000
			res += total_time
		res = res/100
		print(f'Function {func.__name__}{args} {kwargs} Took averagly {res:.4f} ms')
		return result
	return timeit_wrapper


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.profile = Profile.Profile()
        self.data = app_data.og_data
        self.potential_barnaul_profile_full = copy.deepcopy(self.data)
        self.potential_barnaul_profile_full['user_info']['geo_coords'] = (53.354779, 83.769783)
        self.potential_barnaul_profile = app_data.empty_barnaul_profile_data
        self.empty_data = app_data.empty_data

    def test_set_profile_full(self):
        self.profile.set_profile(self.data)
        self.assertEqual(self.profile.tg_id, self.data["tg_id"])
        self.assertTrue(self.profile.active)
        self.assertEqual(self.profile.user_info.name, self.data["user_info"]["name"])
        self.assertEqual(self.profile.user_info.description, self.data["user_info"]["description"])
        self.assertEqual(self.profile.user_info.interests, self.data["user_info"]["interests"])
        self.assertEqual(self.profile.user_info.music, self.data["user_info"]["music"])
        self.assertEqual(self.profile.user_info.pol_coords, self.data["user_info"]["pol_coords"])
        self.assertEqual(self.profile.user_info.geo_coords, self.data["user_info"]["geo_coords"])
        self.assertEqual(self.profile.user_info.age, self.data["user_info"]["age"])
        self.assertEqual(self.profile.user_info.gender, self.data["user_info"]["gender"])
        self.assertEqual(self.profile.user_info.personality, self.data["user_info"]["personality"])
        self.assertEqual(self.profile.user_prefs.age_pref, self.data["user_prefs"]["age_pref"])
        self.assertEqual(self.profile.user_prefs.area_restrict, self.data["user_prefs"]["area_restrict"])
        self.assertEqual(self.profile.user_prefs.goal, self.data["user_prefs"]["goal"])
        self.assertEqual(self.profile.user_prefs.gender_pref, self.data["user_prefs"]["gender_pref"])
        self.assertTrue(self.profile.user_prefs.pol_pref)
        self.assertTrue(self.profile.user_prefs.int_pref)
        self.assertTrue(self.profile.user_prefs.music_pref)
        self.assertTrue(self.profile.user_prefs.loc_pref)
        self.assertTrue(self.profile.user_prefs.pers_pref)

    def test_get_profile_full(self):
        self.profile.set_profile(self.data)
        self.assertEqual(self.profile.get_profile(), self.data)

    def test_set_profile_empty(self):
        self.profile.set_profile(self.empty_data)
        self.assertEqual(self.profile.tg_id, self.empty_data["tg_id"])
        self.assertTrue(self.profile.active)
        self.assertEqual(self.profile.user_info.name, self.empty_data["user_info"]["name"])
        self.assertEqual(self.profile.user_info.description, None)
        self.assertEqual(self.profile.user_info.interests, [])
        self.assertEqual(self.profile.user_info.music, [])
        self.assertEqual(self.profile.user_info.pol_coords, None)
        self.assertEqual(self.profile.user_info.geo_coords, None)
        self.assertEqual(self.profile.user_info.age, self.empty_data["user_info"]["age"])
        self.assertEqual(self.profile.user_info.gender, self.empty_data["user_info"]["gender"])
        self.assertEqual(self.profile.user_info.personality, None)
        self.assertEqual(self.profile.user_prefs.age_pref, (18, 100, 25))
        self.assertEqual(self.profile.user_prefs.area_restrict, 20000)
        self.assertEqual(self.profile.user_prefs.goal, None)
        self.assertEqual(self.profile.user_prefs.gender_pref, None)
        self.assertFalse(self.profile.user_prefs.pol_pref)
        self.assertFalse(self.profile.user_prefs.int_pref)
        self.assertFalse(self.profile.user_prefs.music_pref)
        self.assertFalse(self.profile.user_prefs.loc_pref)
        self.assertFalse(self.profile.user_prefs.pers_pref)

    def test_get_profile_empty(self):
        self.profile.set_profile(self.empty_data)
        expected_empty_data = app_data.none_data
        self.assertEqual(self.profile.get_profile(), expected_empty_data)

    def test_public_data(self):
        my_profile = Profile.Profile()
        my_profile.set_profile(self.data)
        barnaul_profile = Profile.Profile()
        barnaul_profile.set_profile(self.potential_barnaul_profile)
        expected_data = {
            'name': 'Maksim', 
            'distance': 344.8864092006031, 
            'description': 'description', 
            'interests': ['music', 'hiking'], 
            'music': ['Bjork', 'Earl Sweatshit'], 
            'age': 24, 
            'gender': 'male', 
            'photo': None
            }
        self.assertEqual(my_profile.public_data(barnaul_profile.user_info.geo_coords), expected_data)
    
    def test_profile_likeness_calculator(self):
        my_profile = Profile.Profile()
        my_profile.set_profile(self.data)
        barnaul_profile = Profile.Profile()
        barnaul_profile.set_profile(self.potential_barnaul_profile_full)
        profile_calculator = ProfileCalculations.ProfileCalculations(my_profile, None)
        print(profile_calculator.calculate_likeness(barnaul_profile))
        self.assertTrue(profile_calculator.calculate_likeness(barnaul_profile) > 0.90 and profile_calculator.calculate_likeness(barnaul_profile) < 0.93)

        barnaul_profile.set_profile(self.potential_barnaul_profile)
        print(profile_calculator.calculate_likeness(barnaul_profile))
        self.assertTrue(profile_calculator.calculate_likeness(barnaul_profile) > 0.50 and profile_calculator.calculate_likeness(barnaul_profile) < 0.53)

    def test_likeness_sorting(self):
        my_profile = Profile.Profile()
        my_profile.set_profile(self.data)
        potential_profiles = []
        barnaul_profile = Profile.Profile()
        barnaul_profile.set_profile(self.potential_barnaul_profile)
        potential_profiles.append(barnaul_profile)
        almost_me = Profile.Profile()
        almost_me.set_profile(self.data)
        potential_profiles.append(almost_me)
        profile_calculator = ProfileCalculations.ProfileCalculations(my_profile, potential_profiles)
        self.assertEqual(profile_calculator.sort_by_likeness(), [almost_me, barnaul_profile])

class TestProfileDb(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.data = app_data.og_data
        self.potential_match_1_data = copy.deepcopy(self.data)
        self.potential_match_1_data['user_info']['gender'] = 'female'
        self.potential_match_1_data['user_prefs']['gender_pref'] = 'male'
        self.potential_match_1_profile = Profile.Profile(self.potential_match_1_data)
        self.potential_match_1_db = ProfileDb.ProfileDb(self.potential_match_1_profile)
        self.potential_match_1_db.connect()

        self.potential_match_2_data = copy.deepcopy(self.data)
        self.potential_match_2_data['user_info']['gender'] = 'female'
        self.potential_match_2_data['user_prefs']['gender_pref'] = 'male'
        self.potential_match_2_profile = Profile.Profile(self.potential_match_2_data)
        self.potential_match_2_db = ProfileDb.ProfileDb(self.potential_match_2_profile)
        self.potential_match_2_db.connect()

        self.profile = Profile.Profile(self.data)
        self.profile_db = ProfileDb.ProfileDb(self.profile)
        self.profile_db.connect()
        self.profile_db.delete_everything()
        for _ in range (10):
            test_profile = Profile.Profile(self.potential_match_1_data)
            test_profile_db = ProfileDb.ProfileDb(test_profile)
            test_profile_db.connect()
            test_profile_db.save_to_db()
            test_profile_db.disconnect()
    
    def tearDown(self):
        self.profile_db.delete_everything()
        self.profile_db.disconnect()
        self.potential_match_1_db.disconnect()
        self.potential_match_2_db.disconnect()

    def test_set_profile_full(self):
        id = self.profile_db.save_to_db()
        new_profile_db = ProfileDb.ProfileDb()
        new_profile_db.connect()
        profile = new_profile_db.retrieve_from_db(id)
        self.assertEqual(profile.get_profile(), self.profile.get_profile())
        new_profile_db.disconnect()
    
    def test_potential_matches(self):
        id_1 = self.potential_match_1_db.save_to_db()
        id_2 = self.potential_match_2_db.save_to_db()
        id = self.profile_db.save_to_db()
        matches = self.profile_db.potential_matches(id)
        self.assertTrue(id_1, id_2 in [profile.profile_id for profile in matches])
    @timeit
    def test_potential_matches_speed(self):
        # self.profile_db.delete_everything()
        id = self.profile_db.save_to_db()
        profiles = self.profile_db.potential_matches(id)
        print(profiles)
        self.assertEqual(len(profiles), 10)

        '''
        Initial: 51 ms.
        '''


if __name__ == '__main__':
    unittest.main()