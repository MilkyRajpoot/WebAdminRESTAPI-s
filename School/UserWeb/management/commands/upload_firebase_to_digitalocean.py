from django.core.management.base import BaseCommand
from UserWeb.models import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, firestore
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Fetch the service account key JSON file contents
        try:
            cred = credentials.Certificate('njms-2e633-firebase-adminsdk-xozcb-5d4d48927c.json')
            # Initialize the app with a None auth variable, limiting the server's access
            firebase_admin.initialize_app(cred, {'databaseURL': 'https://njms-2e633.firebaseio.com'})
        except ValueError or None:
            #fetching data for unitTest table
            store = firestore.client()
            datas = store.collection(u'unitTest').list_documents()
            print("Wait.. We are uploading data to unitTest table")
            for iteration, item in enumerate(datas):
                print(iteration)
                # data = store.collection(u'unitTest').document(i.id).get()

                # try:
                #     if data:
                #         print(data)
                #         for content in data.to_dict()['field1']:
                #             f = UnitTest(title=content['title'], subject=content['subject'],
                #                          clas=content['class'], reg=content['reg'], questions=content['questions'],
                #                          ansText=content['ansText'], image=content['image'])
                #             f.save()
                # except KeyError:
                #     pass

            # # fetching data for unitCount table
            # store = firestore.client()
            # datas = store.collection(u'unitCount').list_documents()
            # print("Wait.. We are uploading data to unitCount table")
            # for i in datas:
            #     print(i.id)
            #     data = store.collection(u'unitCount').document(i.id).get()
            #     try:
            #         if data:

            #             print(data)
            #             f = UnitCount(title=data.to_dict()['data']['title'], subject=data.to_dict()['data']['subject'],
            #                           reg=data.to_dict()['data']['reg'], counts=data.to_dict()['data']['count'],
            #                           time=data.to_dict()['data']['time'])
            #             f.save()
            #     except KeyError:
            #         pass

            # # fetching data for timedOut table
            # store = firestore.client()
            # datas = store.collection(u'timedOut').list_documents()
            # print("Wait.. We are uploading data to timedOut table")
            # for i in datas:
            #     print(i.id)
            #     data = store.collection(u'timedOut').document(i.id).get()
            #     try:
            #         if data:
            #             print(data)
            #             f = TimedOut(q_count=data.to_dict()['data']['q_count'], reg=data.to_dict()['data']['reg'])
            #             f.save()
            #     except KeyError:
            #         pass

            # # fetching data for optional_unit table
            # store = firestore.client()
            # datas = store.collection(u'optional_unit').list_documents()
            # print("Wait.. We are uploading data to optional_unit table")
            # for i in datas:
            #     print(i.id)
            #     data = store.collection(u'optional_unit').document(i.id).get()
            #     try:
            #         if data:
            #             print(data)
            #             f = OptionalUnit(reg=data.to_dict()['data']['reg'], topic=data.to_dict()['data']['topic'], date=data.to_dict()['data']['date'])
            #             f.save()
            #     except KeyError:
            #         pass
