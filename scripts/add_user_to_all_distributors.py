from models import Distributor, User, DistributorUser


def all_distributor_keys():
    distributor_keys_to_add_to_user = []
    all_distributors = Distributor.query().fetch()
    for each_distributor in all_distributors:
        distributor_keys_to_add_to_user.append(each_distributor.key)

    return distributor_keys_to_add_to_user


def filtered_distributor_keys(user_email):
    user = User.get_or_insert_by_email(user_email)
    all_distributor_users = DistributorUser.query().fetch()
    distributor_keys_to_add_to_user = all_distributor_keys()

    for each_distributor_user in all_distributor_users:
        if each_distributor_user.user_key == user.key:
            distributor_keys_to_add_to_user.remove(each_distributor_user.distributor_key)

    return distributor_keys_to_add_to_user


def add_user_to_remaining_keys(user_email):
    remaining_keys = filtered_distributor_keys(user_email)
    user = User.get_or_insert_by_email(user_email)
    for each_key in remaining_keys:
        user.add_distributor(each_key)
    print "ALL DONE"


def kick_off(user_email):
    if not User.get_by_email(user_email):
        print "ERROR: NO USER WITH THIS NAME"

    else:
        add_user_to_remaining_keys(user_email)


if __name__ == '__main__':
    kick_off("daniel.ternyak@agosto.com")
