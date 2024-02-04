import src.repositories.specialists as repo_specialists


async def get_list(session, specialist_type_id):
    specialists_data_access = repo_specialists.Specialists(session)
    specialists_list = await specialists_data_access.get_many(specialist_type_id)
    return specialists_list
