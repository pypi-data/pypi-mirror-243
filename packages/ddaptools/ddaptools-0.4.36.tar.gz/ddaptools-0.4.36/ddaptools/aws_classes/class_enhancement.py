
from abc import ABC, abstractmethod
from ddaptools.aws_classes.class_helpers import *
from ddaptools.dda_constants import *
from typing import List
from ddaptools.aws_classes.config_mapper_df import ConfigMapper
import pandas as pd
from ddaptools.dda_models import *
import boto3
from urllib.parse import urlparse
import json
import re
from collections import Counter

utils = Utils()


class SourceAdapter(ABC):
    """Transformation for Status Types Interfaces, 
    some might come in json or have different namings, the idea is to convert them
    into the standard interfaces.
    - 2023-10-02 14:15:01: Support for error_count
    """

    def __init__(self) -> None:
        self.reset_errors()

    def reset_errors(self):
        self.error_count = 0
        self.error_messages = []

    @abstractmethod
    def adapt(staging_events: dict)->dict:
        pass

class SalesforceAdapter(SourceAdapter):

    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 1
        super().__init__()

    def adapt(self, staging_events: dict)->dict:
        """Staging event (with 365 details into 365 adapted source.)
        Args:
            staging_events (dict): Converted Staging event.
        """

        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information
        # {__actor_nelson: {user_id: 1, user_organization_id: ..,  }}
        print("organizationQuerier being used", self.organizationQuerier)
        organization_guid = management_api.get_organization_guid()
        self.organizationQuerier.initialization(organization_guid, platform_type = self.platform_id)
        
        organization_params_salesforce  = self.organizationQuerier.getOrganizationParameters_identity()



        # Building the right interface
        new_details = []
        
        for event in management_api.details:
            user_key_salesforce = Utils.NoneSafe(event, "Actor__c")
            
            # if user_key_salesforce is None, or not in organization_params_salesforce, then skip
            if user_key_salesforce is None or user_key_salesforce not in organization_params_salesforce:
                print("Failed at finding of user_key_salesforce", user_key_salesforce)
                self.error_count += 1
                self.error_messages.append("Failed at finding of user_key_salesforce: " + str(user_key_salesforce))
                continue

            user_profile = organization_params_salesforce[user_key_salesforce]
            

            # Repeated variables
            timestamp = Utils.NoneSafe(event, "ActionDate__c")
            
            if timestamp is None:
                print("Failed at finding of timestamp, discontinuing.", timestamp)
                self.error_count += 1
                self.error_messages.append("Failed at finding of timestamp, on SALESFORCE adapter" + str(timestamp))
                continue
                # raise Exception("Timestamp is None (ActionDate__c)")

            tags_str = Utils.NoneSafe(event, "Tags__c")
            # Split by ';'
            tags_list = tags_str.split(";") if tags_str is not None else None

            ## Expected format:
            # [
            #    {
            #       "name":"HIGH",
            #       "label":"High"
            #    },
            #    {
            #       "name":"IN_PROGRESS",
            #       "label":"In Progress"
            #    }
            # ]
            def convert_tag_into(tag):
                upper_cased_undersed_tag = tag.upper().replace(" ", "_")
                titledWithSpaces = tag.replace("_", " ").title()
                
                return {
                    "name": upper_cased_undersed_tag,
                    "label": titledWithSpaces
                }
            tags = [ convert_tag_into(tag) for tag in tags_list ] if tags_list is not None else [] 
            

            fileEvent = EventData(
                user_id=Utils.NoneSafe(user_profile, "user_id"),
                organization_guid=management_api.organization_guid,
                application="SALESFORCE",
                app=Utils.NoneSafe(event, "Object__c"),
                app_type=None,
                operation=Utils.NoneSafe(event, "Activity__c"),
                operation_type=None,
                staging_detail_guid=Utils.NoneSafe(event, "Id"),
                staging_guid=management_api.guid,
                platform_id=self.platform_id,
                organization_id=1,
                local_timezone=None,
                timestamp=timestamp,
                end_time=None,
                timestamp_local=None,
                end_time_local=None,
                duration=Utils.NoneSafe(event, "Duration__c"),
                description=Utils.NoneSafe(event, "Description__c"),
                url=Utils.NoneSafe(event, "URL__c"),
                site=None,
                url_domain=Utils.NoneSafe(event, "Record_Link__c"),
                files=None,
                file_count=None,
                action_type="ACTIVE",
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                sha2=None,
                email_subject=None,
                from_address=None,
                to_address=None,
                email_bcc=None,
                email_cc=None,
                email_imid=None,
                phone_result=None,
                record_url=Utils.NoneSafe(event, "Record_Link__c"),
                recording_url=None,
                record_id=Utils.NoneSafe(event, "RecordId__c"),
                tags=tags,
            )
            new_details.append(fileEvent)
            
        management_api.details = new_details
        return management_api.to_dict()

class ChromeAdapter(SourceAdapter):
    
    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 2
        super().__init__()

    def adapt(self, staging_events: dict)->dict:
        print("Chrome Adapter is being used")
        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information
        # {__actor_nelson: {user_id: 1, user_organization_id: ..,  }}
        organization_guid = management_api.get_organization_guid()
        self.organizationQuerier.initialization(organization_guid, platform_type = self.platform_id)
        
        organization_and_user_params  = self.organizationQuerier.getOrganizationParameters_connectorguid(
            management_api.connector_guid
        )
        print("organization_and_user_params", organization_and_user_params)

        # Building the right interface
        new_details = []
        
        for event in management_api.details:
            user_profile = organization_and_user_params["user_profile"]
            
            # Repeated variables
            timestamp = Utils.NoneSafe(event, "timestamp")
            if(timestamp is None):
                self.error_count += 1
                self.error_messages.append("Failed at finding of timestamp ON CHROME ADAPTER " + str(timestamp))
                continue

            files = Utils.NoneSafe(event, "files")

            def aggregateFileSizes(files):
                
                if(files is None):
                    return 0
                
                total_size = 0
                for file in files:
                    total_size += Utils.NoneSafe(file, "size", 0)
                return total_size
            
            def eventActiveStatus(event):
                """Determines if the event ACTIVITY Status for Chrome Extension if the type it will return ACTIVE unless the event type is idle
                Passive if it is download or upload

                Args:
                    event (str): Event  should contain type key.

                Returns:
                    str: ACTIVE | IDLE | PASSIVE
                """
                # if the type is idle, then it is IDLE
                event_type = Utils.NoneSafe(event, "type")

                if(event_type == "idle"): return "IDLE"
                if(event_type == "download"): return "PASSIVE"
                if(event_type == "upload"): return "PASSIVE"
                return "ACTIVE"
                
            def getSumFeats(dictObject, *args):
                """
                Get the sum of numeric values for the specified keys from the dictionary.
                """
                total = 0
                for key in args:
                    value = dictObject.get(key)
                    if isinstance(value, (int, float)):
                        total += value
                return total
                

            fileEvent = EventData(
                user_id=Utils.NoneSafe(user_profile, "user_id"),
                organization_guid=management_api.organization_guid,
                application="CHROME",
                app=Utils.NoneSafe(event, "domain"),
                app_type=None,
                operation=Utils.NoneSafe(event, "type"),
                operation_type=None,
                staging_detail_guid=Utils.NoneSafe(event, "guid"),
                staging_guid=management_api.guid,
                platform_id=self.platform_id,
                organization_id=Utils.NoneSafe(user_profile, "user_organization_id"),
                local_timezone=Utils.NoneSafe(user_profile, "user_timezone"),
                timestamp=timestamp,
                end_time=Utils.NoneSafe(event, "endTime"),
                timestamp_local=None,
                end_time_local=None,
                duration=None,
                description=Utils.NoneSafe(event, "interactions"),
                url=Utils.NoneSafe(event, "url"),
                site=Utils.NoneSafe(event, "domain"),
                url_domain=Utils.NoneSafe(event, "domain"),
                files=files,
                file_count= len(files) if files is not None else 0,
                action_type=eventActiveStatus(event),
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=aggregateFileSizes(files),
                sha2=None,
                email_subject=None,
                from_address=None,
                to_address=None,
                email_bcc=None,
                email_cc=None,
                email_imid=None,
                phone_result=None,
                record_url=None,
                recording_url=None,
                record_id=None,
                keystrokes=getSumFeats(event, "keyboard"),
                mouse_clicks=getSumFeats(event, " auxclick", "click", ", dbclick"),
                span_sequence=Utils.NoneSafe(event, "spanSequence", 0),
                span_guid=Utils.NoneSafe(event, "spanGUID"),
                span_start = Utils.NoneSafe(event, "spanStartTime", timestamp)

            )
            new_details.append(fileEvent)
        management_api.details = new_details
        return management_api.to_dict()

class WindowsAdapter(SourceAdapter):
    """
    Adapter for windows events
    """
    
    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 3
        super().__init__()

    def adapt(self, staging_events: dict)->dict:
        
        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information

        organization_guid = management_api.get_organization_guid()
        self.organizationQuerier.initialization(organization_guid, platform_type = self.platform_id)
        organization_and_user_params  = self.organizationQuerier.getOrganizationParameters_connectorguid(
            management_api.connector_guid
        )

        # Building the right interface
        new_details = []
        for event in management_api.details:

            try:
                user_profile = organization_and_user_params["user_profile"]
                # It seems that each event is a string here => Convert into json
                # event = json.loads(event_raw_str)
                
                event_type = Utils.NoneSafe(event, "event_type")
                if not event_type:
                    self.error_count += 1
                    self.error_messages.append("Event Type was empty")
                    continue
                
                # Repeated variables
                timestamp = Utils.NoneSafe(event, "event_date")
                if(timestamp is None):
                    self.error_count += 1
                    self.error_messages.append("Failed at finding of timestamp ON WINDOWS ADAPTER " + str(timestamp))
                    continue

                if event_type == "WIN_APP_ACTIVE":
                    if Utils.NoneSafe(event, "name") is None:
                        self.error_count += 1
                        self.error_messages.append("Name is None")
                        continue
                    
                    fileEvent = EventData(
                        user_id=Utils.NoneSafe(user_profile, "user_id"),
                        organization_guid=management_api.organization_guid,
                        application=Utils.NoneSafe(event, "name"),
                        app=Utils.NoneSafe(event, "window_title"),
                        app_type=None,
                        operation=Utils.NoneSafe(event, "activity"),
                        operation_type=None,
                        staging_detail_guid=Utils.NoneSafe(event, "guid"),
                        staging_guid=management_api.guid,
                        platform_id=self.platform_id,
                        organization_id=Utils.NoneSafe(user_profile, "organization_id"),
                        local_timezone=Utils.NoneSafe(user_profile, "user_timezone"),
                        timestamp=timestamp,
                        end_time=Utils.NoneSafe(event, "event_end_date"),
                        timestamp_local=None,
                        end_time_local=None,
                        duration=None,
                        description=Utils.NoneSafe(event, 'description'), #createDescription(event),
                        url=None,
                        site=None, 
                        url_domain=None,
                        files=None,
                        file_count= None,
                        action_type=None, # eventActiveStatus(event),
                        geolocation=None,
                        ipv4=None, #Utils.NoneSafe(network_interface_dict, "ipv4"),
                        local_ipv4=None,
                        size=None,
                        sha2=None,
                        email_subject=None,
                        from_address=None,
                        to_address=None,
                        email_bcc=None,
                        email_cc=None,
                        email_imid=None,
                        phone_result=None,
                        record_url=None,
                        recording_url=None,
                        record_id=None,
                        keystrokes=Utils.NoneSafe(event, "keypresses", 0),
                        mouse_clicks=Utils.NoneSafe(event, "mouseclicks", 0)
                    )
                    new_details.append(fileEvent)

                    
            except Exception as e:
                print(e)
                print("======== Error in Windows Adapter ======== ")
                print(event)
                
                continue
        management_api.details = new_details
        return management_api.to_dict()

class EmailAdapter(SourceAdapter):
    """Current Version notes

    - Only Detects SENDS if not from in identitty it will SKIP
    - Processing to be done here in this version.

    """
    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 4
        super().__init__()
            
    def extract_emails(self, input_string, update_connector_flag = True, getJustOne = False):
        email_pattern = r'\"([^<>,\s^"]+@[^<>,\s]+(?:\s*,\s*[^<>,\s]+@[^<>,\s^"]+)*)"|([^<>,\s^"]+@[^<>,\s]+(?:\s*,\s*[^<>,\s]+@[^<>,\s^"]+)*)'

        # Find all matches using the regex pattern
        matches = re.findall(email_pattern, input_string)
        
        # Extract the first group if it exists, otherwise use the second group
        cleaned_matches = [match[0] if match[0] else match[1] for match in matches]
        
        cleaned_matches = list(set(cleaned_matches))
        
        if getJustOne:
            cleaned_matches = cleaned_matches[0]

        return cleaned_matches


    def extract_email_data(self, input_dict):
        # Extract data from the dictionary structure
        timestamp = input_dict['ses']['mail']['timestamp']
        source = input_dict['ses']['mail']['source']
        messageId = input_dict['ses']['mail']['messageId']
        destination = input_dict['ses']['mail']['destination']
        headers = input_dict['ses']['mail']['headers']

        # Initialize data fields
        date = ""
        from_email = ""
        to = ""
        cc = ""
        subject = ""
        message_id = ""

        # Extract data from headers
        for header in headers:
            name = header['name']
            value = header['value']
            if name == "Date":
                date = value
            elif name == "From":
                from_email = self.extract_emails(value, getJustOne=True)
            elif name == "To":
                to = self.extract_emails(value)
            elif name == "CC":
                cc = self.extract_emails(value)
            elif name == "Subject":
                subject = value
            elif name == "Message-ID":
                message_id = value

        # Create a dictionary to store the extracted data
        extracted_data = {
            "timestamp": timestamp,
            "source": source,
            "messageId": messageId,
            "destination": destination,
            "date": date,
            "from": from_email,
            "to": to,
            "cc": cc,
            "subject": subject,
            "message_id": message_id
        }

        return extracted_data


    def adapt(self, staging_events: dict) -> dict:
        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        organization_guid = management_api.get_organization_guid()

        self.organizationQuerier.initialization(organization_guid, platform_type = self.platform_id)
        identity_profiles = self.organizationQuerier.getOrganizationParameters_identity()
        

        new_details = []
        for raw_event in management_api.details:
            event = self.extract_email_data(raw_event)

            user_profile = None
            from_address = Utils.NoneSafe(event, "from")
            
            if from_address is None:
                raise Exception("From Address is None")

            try:
                user_profile = identity_profiles[from_address]
            except Exception as e:
                raise Exception("User Profile not found for email address: " + str(from_address))
                
            

            fileEvent = EventData(
                
                user_id=Utils.NoneSafe(user_profile, "user_id"),
                organization_guid=management_api.organization_guid,
                application="EMAIL",
                app="EMAIL",
                app_type=None,
                operation="SEND",
                operation_type=None,
                staging_detail_guid=Utils.NoneSafe(event, "guid"),
                staging_guid=management_api.guid,
                platform_id=self.platform_id,
                organization_id=Utils.NoneSafe(user_profile, "user_organization_id"),
                local_timezone=Utils.NoneSafe(user_profile, "user_timezone"),
                timestamp=Utils.NoneSafe(event, "timestamp"),
                end_time=Utils.NoneSafe(event, "timestamp"),
                timestamp_local=None,
                end_time_local=None,
                duration=None,
                description=None,
                url=None,
                site=None,
                url_domain=None,
                files=None,
                file_count=None,
                action_type="ACTIVE",
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                sha2=None,
                email_subject=Utils.NoneSafe(event, "subject"),
                from_address=Utils.NoneSafe(event, "from"),
                to_address=Utils.NoneSafe(event, "to"),
                email_bcc=Utils.NoneSafe(event, "bcc"),
                email_cc=Utils.NoneSafe(event, "cc"),
                email_imid=Utils.NoneSafe(event, "message_id"),
                phone_result=None,
                record_url=None,
                recording_url=None,
                record_id=None,
                keystrokes=None,
                mouse_clicks=None,
                span_guid=Utils.NoneSafe(event, 'span_guid'),
                span_start=Utils.NoneSafe(event, 'span_guid')
                
            )
            
            print("email adapter new details", fileEvent.__dict__)
            new_details.append(fileEvent)

        management_api.details = new_details
        return management_api.to_dict()



class TransformationStrategy(ABC):
    """Transformation Strategy to be implemented
    """
    
    @abstractmethod
    def publish(self, enhanced_events: List[dict]):
        pass


    @abstractmethod
    def transform(self, staging_events_events: List[dict]) -> List[dict]: 
        pass

class BasicEnhancement(TransformationStrategy):
    """
    Basic Enhancemnts involves the following:
    (1) Update based on the appropriate source
    (2) Enhance it using the specific business specifications
    (3) Publish it into the events database
    """
    
    def __init__(self, source_adapter, organizationDBProvider: OrganizationalQuerier, publishingDBProvider: DatabaseProvider):
        

        self.organizationDBProvider = organizationDBProvider
        self.publishingDBProvider = publishingDBProvider
        self.default_source_adapter = source_adapter
        self.staging_event_guid = None # Populated at the transform method
        

        # Here it works just fine.
        # But then the problem is with the source_adpaters that doesnt work

        self.businessRules = {} # To be populated when enhancements is requested.
        self.error_count = 0
        self.error_messages = []
        self.default_source_adapter.reset_errors()

    def transform(self, staging_events_events: List[dict]) -> dict["events": List[Event], "timeslots": List[Timeslot]]: 
        print('transform called ________________________________')
        print('transform called with count', len(staging_events_events))
        standarized_events:StagingModel = self.adapt(staging_events_events)
        enhanced_events: dict["events": List[Event], "timeslots": List[Timeslot]] = self.businessEnhancements(standarized_events)
        self.staging_event_guid = standarized_events["guid"]
        return enhanced_events
    
    def separateEvent(self, events: List[dict]) -> dict:
        """
            produce two list of events:
            (1) events mapped
            (2) timeslot mappedimage.png
            In the future there is another process that also cretes the timeslots separated on between.
            @param events: List of events in format of dict with the same properties of EventData model.
            @return: dict of events and timeslots: dict{event: List[Event], timeslot: List[Timeslot]}
        """
        events_list = []
        timeslots_list = []

        for event in events:
            eventData = Utils.eventDataIntoTimeSlots(event)
            timeslots_list.extend(eventData)
            
            # Always create an event based event.
            new_event = Event.from_dict(event)
            events_list.append(new_event.to_dict())

        return {
            "events": events_list,
            "timeslots": timeslots_list
        }


    def businessEnhancements(self, events: StagingModel) -> dict["events": List[Event], "timeslots": List[Timeslot]]:
        """
        Args:
            events (dict): events of the business enhancment.

        Returns:
            @return: dict of events and timeslots: dict{event: List[Event], timeslot: List[Timeslot]}
        """
        print("business enhancement input count:", len(events["details"]))
        
        normalized_events: List[dict] = ConfigMapper.event_normalization(events)
        
        print("Normalized Events:", len(normalized_events))
        
        organization_params: List[dict] = self.organizationDBProvider.getOrganizationParameters()
        print("organization_params", len(organization_params))
        
        
        joint_events: List[dict] = ConfigMapper.join_organization_fields(
            normalized_events=normalized_events,
            user_information_table=organization_params
        )
        print("joint_events", len(joint_events))

        if(len(joint_events)):
            print("joint event business", joint_events[0])

        date_mapped_events = ConfigMapper.date_related_population(join_events=joint_events)
        

        # Convert into pandas first.
        # date_mapped_events_df = pd.DataFrame(date_mapped_events)
        processed_events = ConfigMapper.categorization_jobs(date_mapped_events=date_mapped_events)
        # processed_events = classified_events_df
        # print("processed event", processed_events[0])
        
        # Have the separatation between events and timeslots
        # print("2 | events_list", len(processed_events["evemts"]), "timeslots_list", len(processed_events["timeslots"]))
        return self.separateEvent(processed_events)



    def adapt(self, staging_events: dict) -> dict:
        res = self.default_source_adapter.adapt(staging_events = staging_events)
        
        self.error_count += self.default_source_adapter.error_count
        self.error_messages.extend(self.default_source_adapter.error_messages)

        return res

    def publish(self, enhanced_events: dict["events": List[dict], "timeslot": List[dict]], table_name=""):
        print("publishing events count:", len(enhanced_events["events"]))
        self.publishingDBProvider.publish(enhanced_events, table_name=table_name)
        unique_error_string = ""
        if(len(self.error_messages)):
            error_counts = Counter(self.error_messages)
            unique_error_string = "     ".join([f"{count} - {error}" for error, count in error_counts.items()])
            print("unique_error_string", unique_error_string)

        self.publishingDBProvider.update_status_staging(staging_event_guid=self.staging_event_guid, 
                                                        status="PROCESSED", 
                                                        processed_item_count=len(enhanced_events["events"]),
                                                        processing_error_count=self.error_count,
                                                        processing_error_sample=unique_error_string)

    def fetchBusinessRules():
        """Using the self.organizationDBProvider it receives and updates the Dataset
        """
        pass

class PostgresS3ConnectorBasedCommonProcessor():
    """v6 of the common processor
    Fixes:
    - Now it finds the details through the postgres database (location) and s3 (details.json). 
    - However it should still be compatible with details missings.
    """
    def __init__(self, publishingDBProvider: DatabaseProvider, organization_provider: OrganizationalQuerier, job_parameters: dict):
        self.publishingDBProvider = publishingDBProvider
        self.job_parameters = job_parameters

        # Because we dont know how it will look on the future, it would look like { event_guid }
        self.organization_provider = organization_provider

    def runJobs(self):
        """Runs the jobs it was instantiated with. by analizing first which is the job type required
        """
  
        try:
            ERROR_STATUS = "ERROR - STAGING EVENT"
            specific_staging_event: List[dict] = self.getStagingEvent()


            ERROR_STATUS = "ERROR - GET TRANSFORMATION STRATEGY"
            transformationStrategy = self.getTransformationStrategy(specific_staging_event)

            ERROR_STATUS = "ERROR - TRANSFORMATION"
            enhanced_events: List[dict] = transformationStrategy.transform(specific_staging_event)

            
            ERROR_STATUS = "ERROR - PUBLISHING"
            transformationStrategy.publish(enhanced_events=enhanced_events)
        except Exception as e:
            print("error Detected")
            self.publishingDBProvider.update_status_staging(staging_event_guid=self.job_parameters[EVENT_GUID], status= ERROR_STATUS)
            raise Exception("Error while processing the job", ERROR_STATUS )
        


    def getStagingEvent(self) -> List[dict]:
        """Depending on the job parameters it receives the events from either The Provider and either Table.
        I am as
        """
        staging_event_row = self.publishingDBProvider.getOne(key_value=self.job_parameters[EVENT_GUID], status="PROCESSING") # Gets the first one with that GUID
        
        s3_key = staging_event_row["s3_key"]
        if(s3_key is not None  or s3_key != ""):
            # extract the details.json
            s3_resource = boto3.resource('s3')
            parsed_url = urlparse(s3_key)
            bucket_name = parsed_url.netloc
            object_key = parsed_url.path.lstrip("/")
            

            # Retrieve the JSON object from S3
            s3_object = s3_resource.Object(bucket_name, object_key)
            print("object_key", object_key, "bucket_name", bucket_name, "s3_key", 
                  s3_key, "parsed_url", 
                  parsed_url, "s3_object", s3_object)
            json_data = s3_object.get()['Body'].read().decode('utf-8')

            # Parse the JSON data
            parsed_json = json.loads(json_data)
            staging_event_row["details"] = parsed_json

        return staging_event_row
    
    def getTransformationStrategy(self, staging_event) -> TransformationStrategy:
        """Understanding the transformation that is provided by the item. We want to make the transformation later on.
        The idea is toreceive the getTransformationStrategy on the project.
        """

        salesforce_adapter = SalesforceAdapter(organizationQuerier=self.organization_provider)
        chrome_adapter = ChromeAdapter(organizationQuerier=self.organization_provider)
        windows_adapter = WindowsAdapter(organizationQuerier=self.organization_provider)
        email_adapter = EmailAdapter(organizationQuerier=self.organization_provider)

        platform_id = self.organization_provider.get_platform_id(staging_event[CONNECTOR_GUID])
        print("Platform selected", platform_id, "using the connector guid", staging_event[CONNECTOR_GUID])
        platform_map = {
            1: salesforce_adapter,
            2: chrome_adapter,
            3: windows_adapter,
            4: email_adapter
        }

        adapter = None
        
        adapter = platform_map[platform_id]

        basic_enhancment = BasicEnhancement(
            organizationDBProvider=self.organization_provider,
            publishingDBProvider=self.publishingDBProvider,
            source_adapter=adapter
        )

        return basic_enhancment










