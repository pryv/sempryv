from semantic.domain_models import sempryv_models as db


class SempryvDataProvider:
    def __init__(self):
        self.db = db

    def exists_user(self, username: str):
        model = self.db.Users
        count = self.db.session.query(model.username, model.token).filter(model.username == username).count()
        if count == 1:
            return True
        return False

    def insert_new_user(self, username, token):
        new_user = self.db.Users(username=username, token=token)
        self.db.session.add(new_user)
        try:
            self.db.session.commit()
            self.db.session.flush()
        except Exception(e):
            print('error: {}'.format(e))
            self.db.session.rollback()

    def get_all_users(self):
        model = self.db.Users
        rows = self.db.session.query(model.username, model.token).all()
        return rows

    def persist_models(self, file):
        model = self.db.AnalyticsModels
        # new_model = self.db.AnalyticsModels(classifier=)

        pass