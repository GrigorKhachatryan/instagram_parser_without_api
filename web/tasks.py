from user_data import Information


def insta_tasks(login):
    obj = Information(nickname=login)
    country_code = obj.similar_users()
    return country_code
