# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import shutil

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.readsutilsClient import ReadsUtils
from .Utils.run_LighterUtils import run_lighter, upload_reads
from .Utils.createHtmlReport import HTMLReportCreator

#END_HEADER


class dan_hoppLighter:
    '''
    Module Name:
    dan_hoppLighter

    Module Description:
    A KBase module: dan_hoppLighter
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_dan_hoppLighter(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_dan_hoppLighter
        logging.info('Running run_dan_hoppLighter with params=' + str(params))
        logging.info('Downloading reads from ' + params['input_reads_ref'])

        # These three lines allow it to download a reads-type file that would be in the narrative
        ru = ReadsUtils(self.callback_url)
        input_file_info = ru.download_reads({'read_libraries': [params['input_reads_ref']],
                                             'interleaved': 'true'})['files'][params['input_reads_ref']]
        logging.info('Downloaded reads from ' + str(input_file_info))

        output_reads_name = params['output_reads_name']
        output_reads_file = output_reads_name + ".fq"
        logging.info('Output reads name: ' + output_reads_file)

        #Lighter
        logging.info('Running Lighter')
        # Note that the run_lighter function is writing the console output to a location specified by the output_file parameter, not by Lighter's -od parameter.
        # "Results" are corrected files. "Reports" is, well, reports. Make a reportDirectory var. That gets passed into report_creator.create_html_report later on below.
        reportDirectory = os.path.join(self.shared_folder, 'Reports')
        reportFile = os.path.join(self.shared_folder, reportDirectory, 'index.html')
        resultsDirectory = os.path.join(self.shared_folder, 'Results')
        
        # # Get the path from input_file_info['files']['fwd']
        input_file_path = os.path.join(input_file_info['files']['fwd'])
        logging.info('Input file path: ' + input_file_path)

        returned_dict = run_lighter(input_file_path, resultsDirectory, reportFile, params['kmer_length'], params['genome_size'])
        logging.info('Returned dictionary: ' + str(returned_dict))

        corrected_file_path = returned_dict['corrected_file_path']
        logging.info('Corrected file path: ' + corrected_file_path)
 
        # Rename Lighter's output file via a copy
        output_reads_filepath = os.path.join(resultsDirectory, output_reads_file)
        shutil.copy(corrected_file_path, output_reads_filepath)

        isInterleaved = 0 if input_file_info['files']['type'] == 'single' else 1 if input_file_info['files']['type'] == 'interleaved' else None

        new_reads_upa = upload_reads(self.callback_url, output_reads_filepath, params['workspace_name'], output_reads_name, params['input_reads_ref'], isInterleaved)

        # Delete temp files (upload_reads should have already uploaded the corrected file)
        if os.path.exists(resultsDirectory):
            shutil.rmtree(resultsDirectory)

        objects_created = [{
                'ref': new_reads_upa,
                'description': 'Corrected reads library'
            }]

        # Create a report
        report_creator = HTMLReportCreator(self.callback_url)
        output = report_creator.create_html_report(reportDirectory, params['workspace_name'], objects_created)
        logging.info ('HTML output report: ' + str(output))

        # 1st iteration/default report:
        # report = KBaseReport(self.callback_url)
        # report_info = report.create({'report': {'objects_created':[],
        #                                         'text_message': params['input_reads_ref']},
        #                                         'workspace_name': params['workspace_name']})
        # output = {
        #     'report_name': report_info['name'],
        #     'report_ref': report_info['ref'],
        # }
        # logging.info('Output object: ' + str(output))
        #END run_dan_hoppLighter

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_dan_hoppLighter return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
