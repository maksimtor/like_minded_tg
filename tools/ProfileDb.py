import psycopg2
from tools import Profile
from ast import literal_eval as make_tuple

class ProfileDb:
    def __init__(self, profile=None):
        if profile:
            self.profile = profile
        else:
            self.profile = Profile.Profile()
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname='like_minded_match', 
                    user='lmm_user', 
                    password='lmm_user', 
                    host='localhost'
                    )
            except psycopg2.DatabaseError as e:
                raise e
            finally:
                pass
                # print('Connection opened successfully.')

    def disconnect(self):
        """Connect to a Postgres database."""
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
            except psycopg2.DatabaseError as e:
                raise e
            finally:
                pass
                # print('Connection closed successfully.')

    def save_to_db(self):
        with self.conn.cursor() as cursor:
            insert_user_prefs_sql = '''
                            insert into user_prefs 
                            (age_pref, pol_pref, int_pref, music_pref, loc_pref, pers_pref, area_restrict, goal, gender_pref)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;
                            '''
            cursor.execute(insert_user_prefs_sql, 
                           (
                            self.profile.user_prefs.age_pref, 
                            self.profile.user_prefs.pol_pref, 
                            self.profile.user_prefs.int_pref, 
                            self.profile.user_prefs.music_pref,
                            self.profile.user_prefs.loc_pref,
                            self.profile.user_prefs.pers_pref,
                            self.profile.user_prefs.area_restrict,
                            self.profile.user_prefs.goal,
                            self.profile.user_prefs.gender_pref))
            user_prefs_id = cursor.fetchone()[0]
            insert_user_info_sql = '''
                            insert into user_info 
                            (name, description, interests, music, pol_coords, 
                            geo_coords, age, gender, personality)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;
                            '''
            cursor.execute(insert_user_info_sql, 
                           (
                            self.profile.user_info.name, 
                            self.profile.user_info.description, 
                            self.profile.user_info.interests, 
                            self.profile.user_info.music,
                            self.profile.user_info.pol_coords,
                            self.profile.user_info.geo_coords,
                            self.profile.user_info.age,
                            self.profile.user_info.gender,
                            self.profile.user_info.personality))
            # cursor.execute('''insert into photos (pic) values (%s)''', self.profile.photo)
            user_info_id = cursor.fetchone()[0]
            insert_user_sql = '''
                            insert into profiles 
                            (tg_id, active, user_info_id, user_prefs_id, photo_id)
                            values (%s, %s, %s, %s, %s) returning profile_id;
                            '''
            cursor.execute(insert_user_sql, 
                           (
                            self.profile.tg_id, 
                            self.profile.active, 
                            user_info_id,
                            user_prefs_id,
                            None))
            self.conn.commit()
            return cursor.fetchone()[0]
    def retrieve_from_db(self, id):
            with self.conn.cursor() as cursor:
                select_profile = '''
                                select * from profiles 
                                join user_info on profiles.user_info_id=user_info.id
                                join user_prefs on profiles.user_prefs_id=user_prefs.id
                                where profile_id = %s;
                                '''
                cursor.execute(select_profile, (id,))
                data = list(cursor.fetchone())
                columns = list(map(lambda x: x[0], cursor.description))
                user_data = dict(zip(columns, list(data)))
                user_data['pol_coords'] = make_tuple(user_data['pol_coords'])
                user_data['geo_coords'] = make_tuple(user_data['geo_coords'])
                user_data['personality'] = make_tuple(user_data['personality'])
                user_data['age_pref'] = make_tuple(user_data['age_pref'])
                self.profile.set_profile(user_data)
                return self.profile

    def potential_matches(self, id):
            with self.conn.cursor() as cursor:
                select_profiles = '''
                                select p2.*, ui2.*, up2.* from 
                                profiles p1 
                                join user_info as ui1 on p1.user_info_id = ui1.id
                                join user_prefs as up1 on p1.user_prefs_id = up1.id, 
                                profiles p2
                                join user_info as ui2 on p2.user_info_id = ui2.id
                                join user_prefs as up2 on p2.user_prefs_id = up2.id
                                where 
                                p1.tg_id = %s or p1.profile_id = %s and
                                (up1.goal is null or up1.goal = up2.goal) and
                                (up2.goal is null or up1.goal = up2.goal) and

                                (up1.gender_pref is null or up1.gender_pref = ui2.gender) and
                                (up2.gender_pref is null or up2.gender_pref = ui1.gender) and

                                (((up1.age_pref).min_age <= ui2.age and (up1.age_pref).max_age >= ui2.age)) and
                                (((up2.age_pref).min_age <= ui1.age and (up2.age_pref).max_age >= ui1.age)) and

                                (up1.area_restrict>distance((ui1.geo_coords).lat, (ui1.geo_coords).lon, (ui2.geo_coords).lat, (ui2.geo_coords).lon)) and
                                (up2.area_restrict>distance((ui1.geo_coords).lat, (ui1.geo_coords).lon, (ui2.geo_coords).lat, (ui2.geo_coords).lon))
                                ;
                                '''
                cursor.execute(select_profiles, (str(id), id))
                data = list(cursor.fetchall())
                profiles = []
                for row in data:
                    columns = list(map(lambda x: x[0], cursor.description))
                    user_data = dict(zip(columns, list(row)))
                    user_data['pol_coords'] = make_tuple(user_data['pol_coords'])
                    user_data['geo_coords'] = make_tuple(user_data['geo_coords'])
                    user_data['personality'] = make_tuple(user_data['personality'])
                    user_data['age_pref'] = make_tuple(user_data['age_pref'])
                    profiles.append(Profile.Profile(data = user_data))
                return profiles
    
    def delete_everything(self):
            with self.conn.cursor() as cursor:
                delete_profiles = '''delete from profiles cascade;'''
                delete_user_info = '''delete from user_info cascade;'''
                delete_user_prefs = '''delete from user_prefs cascade;'''
                cursor.execute(delete_profiles)
                cursor.execute(delete_user_info)
                cursor.execute(delete_user_prefs)
                self.conn.commit()
    
    def update_profile(self, profile):
        #TODO
        pass