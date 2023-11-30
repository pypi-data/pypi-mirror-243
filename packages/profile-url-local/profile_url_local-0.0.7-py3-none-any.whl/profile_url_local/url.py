class URL:
    def __init__(self, url_id, profile_id):
        self.profile_id = profile_id
        self.url_id = url_id

    def __dict__(self):
        return {
            'profile_id': self.profile_id,
            'url_id': self.url_id
        }
