import os
from google.cloud import logging
import google.auth

class GcpLogging:
    """Instantiate Google Cloud Logging client.
    """
    def __init__(self, credential_file=None, proxy=''):
        """Instantiate Google Cloud Logging client.

        Args:
            credential_file (str): Credential file path. Default: None
            proxy (str): Proxy URL. Default: ''
        """
        if credential_file is not None:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_file
        if proxy != '':
            os.environ['HTTPS_PROXY'] = proxy
        self.client = logging.Client()
        
    def list_logs(self, project_id, filter_str=None):
        """
        List logs in a project.

        Args:
            project_id (str): Project ID
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'
            
        Returns:
            result (list): List of logs
        """
        logs = self.client.list_logs(project_id=project_id, filter_=filter_str)
        return logs
    
    def list_entries(self, project_id, filter_str=None):
        """
        List log entries in a project.

        Args:
            project_id (str): Project ID
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (list): List of log entries
        """
        entries = self.client.list_entries(project_id=project_id, filter_=filter_str)
        return entries
    
    def write_log(self, project_id, log_name, resource, labels, text_payload=None, json_payload=None):
        """
        Write a log entry.

        Args:
            project_id (str): Project ID
            log_name (str): Log name. Example: 'my-log'
            resource (dict): Resource. Example: {'type': 'global'}
            labels (dict): Labels. Example: {'env': 'dev', 'app': 'my-app'}
            text_payload (str): Text payload. Example: 'my log message'
            json_payload (dict): JSON payload. Example: {'message': 'my log message'}
            
        Returns:
            result (str): It returns 'OK' when successful
        """
        logger = self.client.logger(log_name)
        logger.log_text(text_payload, resource=resource, labels=labels)
        logger.log_struct(json_payload, resource=resource, labels=labels)
        results = 'OK'
        return results
    
    def delete_log(self, project_id, log_name):
        """
        Delete a log.

        Args:
            project_id (str): Project ID
            log_name (str): Log name. Example: 'my-log'

        Returns:
            result (str): It returns 'OK' when successful
        """
        logger = self.client.logger(log_name)
        logger.delete()
        results = 'OK'
        return results
    
    def delete_many_logs(self, project_id, filter_str=None):
        """
        Delete multiple logs.

        Args:
            project_id (str): Project ID
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (str): It returns 'OK' when successful
        """
        logs = self.client.list_logs(project_id=project_id, filter_=filter_str)
        for log in logs:
            log.delete()
        results = 'OK'
        return results
    
    def delete_log_entries(self, project_id, filter_str=None):
        """
        Delete log entries.

        Args:
            project_id (str): Project ID
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (str): It returns 'OK' when successful
        """
        entries = self.client.list_entries(project_id=project_id, filter_=filter_str)
        for entry in entries:
            entry.delete()
        results = 'OK'
        return results
    
    def delete_many_log_entries(self, project_id, filter_str=None):
        """
        Delete multiple log entries.

        Args:
            project_id (str): Project ID
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (str): It returns 'OK' when successful
        """
        entries = self.client.list_entries(project_id=project_id, filter_=filter_str)
        for entry in entries:
            entry.delete()
        results = 'OK'
        return results
    
    def list_sinks(self, project_id):
        """
        List sinks in a project.

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of sinks
        """
        sinks = self.client.list_sinks(project_id=project_id)
        return sinks
    
    def create_sink(self, project_id, sink_name, filter_str, destination):
        """
        Create a sink.

        Args:
            project_id (str): Project ID
            sink_name (str): Sink name. Example: 'my-sink'
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'
            destination (dict): Destination. Example: {'writer_identity': 'serviceAccount:

        Returns:
            result (str): It returns 'OK' when successful
        """
        sink = self.client.sink(sink_name, filter_=filter_str, destination=destination)
        sink.create()
        results = 'OK'
        return results
    
    def delete_sink(self, project_id, sink_name):
        """
        Delete a sink.

        Args:
            project_id (str): Project ID
            sink_name (str): Sink name. Example: 'my-sink'

        Returns:
            result (str): It returns 'OK' when successful
        """
        sink = self.client.sink(sink_name)
        sink.delete()
        results = 'OK'
        return results
    
    def delete_many_sinks(self, project_id):
        """
        Delete multiple sinks.

        Args:
            project_id (str): Project ID

        Returns:
            result (str): It returns 'OK' when successful
        """
        sinks = self.client.list_sinks(project_id=project_id)
        for sink in sinks:
            sink.delete()
        results = 'OK'
        return results
    
    def get_sink(self, project_id, sink_name):
        """
        Get a sink.

        Args:
            project_id (str): Project ID
            sink_name (str): Sink name. Example: 'my-sink'

        Returns:
            result (dict): Sink
        """
        sink = self.client.sink(sink_name)
        return sink
    
    def update_sink(self, project_id, sink_name, filter_str, destination):
        """
        Update a sink.

        Args:
            project_id (str): Project ID
            sink_name (str): Sink name. Example: 'my-sink'
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'
            destination (dict): Destination. Example: {'writer_identity': 'serviceAccount:

        Returns:
            result (str): It returns 'OK' when successful
        """
        sink = self.client.sink(sink_name, filter_=filter_str, destination=destination)
        sink.update()
        results = 'OK'
        return results
    
    def list_exclusions(self, project_id):
        """
        List exclusions in a project.

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of exclusions
        """
        exclusions = self.client.list_exclusions(project_id=project_id)
        return exclusions
    
    def create_exclusion(self, project_id, exclusion_name, filter_str):
        """
        Create an exclusion.

        Args:
            project_id (str): Project ID
            exclusion_name (str): Exclusion name. Example: 'my-exclusion'
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (str): It returns 'OK' when successful
        """
        exclusion = self.client.exclusion(exclusion_name, filter_=filter_str)
        exclusion.create()
        results = 'OK'
        return results
    
    def delete_exclusion(self, project_id, exclusion_name):
        """
        Delete an exclusion.

        Args:
            project_id (str): Project ID
            exclusion_name (str): Exclusion name. Example: 'my-exclusion'

        Returns:
            result (str): It returns 'OK' when successful
        """
        exclusion = self.client.exclusion(exclusion_name)
        exclusion.delete()
        results = 'OK'
        return results
    
    def delete_many_exclusions(self, project_id):
        """
        Delete multiple exclusions.

        Args:
            project_id (str): Project ID

        Returns:
            result (str): It returns 'OK' when successful
        """
        exclusions = self.client.list_exclusions(project_id=project_id)
        for exclusion in exclusions:
            exclusion.delete()
        results = 'OK'
        return results
    
    def get_exclusion(self, project_id, exclusion_name):
        """
        Get an exclusion.

        Args:
            project_id (str): Project ID
            exclusion_name (str): Exclusion name. Example: 'my-exclusion'

        Returns:
            result (dict): Exclusion
        """
        exclusion = self.client.exclusion(exclusion_name)
        return exclusion
    
    def update_exclusion(self, project_id, exclusion_name, filter_str):
        """
        Update an exclusion.

        Args:
            project_id (str): Project ID
            exclusion_name (str): Exclusion name. Example: 'my-exclusion'
            filter_str (str): Filter string. Example: 'resource.type="bigquery_resource"'

        Returns:
            result (str): It returns 'OK' when successful
        """
        exclusion = self.client.exclusion(exclusion_name, filter_=filter_str)
        exclusion.update()
        results = 'OK'
        return results
    
    def list_monitored_resource_descriptors(self, project_id):
        """
        List monitored resource descriptors in a project.

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of monitored resource descriptors
        """
        descriptors = self.client.list_monitored_resource_descriptors(project_id=project_id)
        return descriptors
    
    def get_monitored_resource_descriptor(self, project_id, descriptor_name):
        """
        Get a monitored resource descriptor.

        Args:
            project_id (str): Project ID
            descriptor_name (str): Descriptor name. Example: 'my-descriptor'

        Returns:
            result (dict): Monitored resource descriptor
        """
        descriptor = self.client.monitored_resource_descriptor(descriptor_name)
        return descriptor
    
    def list_metric_descriptors(self, project_id):
        """
        List metric descriptors in a project.

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of metric descriptors
        """
        descriptors = self.client.list_metric_descriptors(project_id=project_id)
        return descriptors
    
    def get_metric_descriptor(self, project_id, descriptor_name):
        """
        Get a metric descriptor.

        Args:
            project_id (str): Project ID
            descriptor_name (str): Descriptor name. Example: 'my-descriptor'

        Returns:
            result (dict): Metric descriptor
        """
        descriptor = self.client.metric_descriptor(descriptor_name)
        return descriptor
    
    def list_logs_based_metrics(self, project_id):
        """
        List logs-based metrics in a project.

        Args:
            project_id (str): Project ID

        Returns:
            result (list): List of logs-based metrics
        """
        metrics = self.client.list_logs_based_metrics(project_id=project_id)
        return metrics
    
    def get_logs_based_metric(self, project_id, metric_name):
        """
        Get a logs-based metric.

        Args:
            project_id (str): Project ID
            metric_name (str): Metric name. Example: 'my-metric'

        Returns:
            result (dict): Logs-based metric
        """
        metric = self.client.logs_based_metric(metric_name)
        return metric
    
