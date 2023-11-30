from ddaptools.aws_classes.class_enhancement import *
from ddaptools.dda_constants import *


def run_procesing(staging_guid = "42c6cd4b-a6ea-4087-ab6a-b8b5bed8b256"):
    """
    1. Email event.
    2. Publishes in database should result in updated start and updated endtime.
    """
    

    credentials = {
        'USERNAME': "postgres",
        'PASSWORD': "dDueller123araM=!",
        "HOST": "test-ddanalytics-rds-v2.cpcwi20k2qgg.us-east-1.rds.amazonaws.com",
        "DB": "v1_2"
    }

    settings = {
        "GET_TABLENAME": "staging_events",
        "TABLENAME_EVENTS": "event",
        "COLUMN_NAMES_EVENTS": Event.get_attribute_keys(),
        "TABLENAME_TIMESLOTS": "timeslot",
        "COLUMN_NAMES_TIMESLOTS": Timeslot.get_attribute_keys()
    }

    
    organizationDBProvider = PostgresqlOrganizationQuerier(credentials=credentials)

    publishingDBProvider = PostgreSQLProviderTimeSlotPlusEventsPublishing(credentials=credentials, settings=settings)

    # Salesforce Sample:  588e876e-31e6-91d4-863f-e0986fd90dad
    processor = PostgresS3ConnectorBasedCommonProcessor(
        
        job_parameters={"guid": staging_guid},
        organization_provider=organizationDBProvider,
        publishingDBProvider=publishingDBProvider
    ) 
    
    processor.runJobs() # Should also post at the Mock Database




def test_multiple():
    staging_list = [
        # '8d908be7-95d9-4edf-a355-6f817f6587ec'
        # 'd1cbca0a-e74f-46c3-849d-972d4c486b83'
        # '387f2a2b-0d2f-443d-be42-500ff304ef38'
        # '014bb5b2-60ed-494e-a5d0-507efb63592e',
        # 'dca4d47f-12b5-4946-acd3-c402d53b567a',
        # 'e5e4b6f2-032e-4e33-a588-f429fe7f7a2f'
        # '72ed2149-4c74-4bd5-afa5-02dff38f961d'
        # '615d99cc-2f87-4bdb-bb93-1653c2809c1c'
        # '7c8eb2c1-461d-4520-8c9d-162edb936817'
        '51e84307-7579-473b-bff5-e61964e64bc5'
    ]

    for staging_guid in staging_list:
        print("Processing: ", staging_guid)
        run_procesing(staging_guid=staging_guid)






