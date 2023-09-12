field_next_question = {
	'name': 'Опиши себя!',
	'description': 'Перечисли свои интересы!',
	'interests': 'Какую музыку любишь?', 
 	'music': 
 		'Какие у тебя политические координаты? \
		Пожалуйста, ответь в формате "-5, 5", \
		где первое число от -10 до +10 означает твое \
		положение по горизонтальной оси, а второе по вертикальной', 
 	'pol_coords': 'Можешь дать теперь просто координаты свои?',
	'geo_coords': 'Сколько тебе лет?', 
 	'age': 'Твой пол?',
	'gender': 'Тип личности?',
	'personality': 'Какой возраст интересен?', 
 	'age_pref': 'Хочешь ограничить территорию?', 
	'area_restrict': 'Пол?', 
    'gender_pref': 'Цель?',
    'goal': ''}


og_data = {
            "tg_id": "tg_id",
            "active": True,
            "user_info": {
                "name": "Maksim",
                "description": "description",
                "interests": ["music", "hiking"],
                "music": ["Bjork", "Earl Sweatshit"],
                "pol_coords": (-5, 5),
                "geo_coords": (52.9978, 78.6449),
                "age": 24,
                "gender": "male",
                "personality": (5, 5, 5, 5, 5)
            },
            "user_prefs": {
                "age_pref": (23, 28, 26),
                "area_restrict": 100,
                "goal": "romantic",
                "gender_pref": "female",
                "pol_pref": True,
                "int_pref": True,
                "music_pref": True,
                "loc_pref": True,
                "pers_pref": True,
            },
            "photo": None
        }

empty_barnaul_profile_data = {
            "tg_id": "tg_id",
            "user_info": {
                "name": "Maksim",
                "age": 24,
                "gender": "male",
                "geo_coords": (53.354779, 83.769783),
            },
            "user_prefs": {
                "pol_pref": False,
                "int_pref": False,
                "music_pref": False,
                "loc_pref": False,
                "pers_pref": False,
            },
            "photo": None
        }

empty_data = {
            "tg_id": "tg_id",
            "user_info": {
                "name": "Maksim",
                "age": 24,
                "gender": "male",
            },
            "user_prefs": {
                "pol_pref": False,
                "int_pref": False,
                "music_pref": False,
                "loc_pref": False,
                "pers_pref": False,
            },
            "photo": None
        }

none_data = {
            "tg_id": "tg_id",
            "active": True,
            "user_info": {
                "name": "Maksim",
                "description": None,
                "interests": [],
                "music": [],
                "pol_coords": None,
                "geo_coords": None,
                "age": 24,
                "gender": "male",
                "personality": None
            },
            "user_prefs": {
                "age_pref": (18, 100, 25),
                "area_restrict": 20000,
                "goal": None,
                "gender_pref": None,
                "pol_pref": False,
                "int_pref": False,
                "music_pref": False,
                "loc_pref": False,
                "pers_pref": False,
            },
            "photo": None
        }
