# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.readsutilsClient import ReadsUtils
from .Utils.run_LighterUtils import run_lighter
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

        #Lighter
        logging.info('Running Lighter')
        # Note that the run_lighter function is writing the console output to a location specified by the output_file parameter, not by Lighter's -od parameter.
        outputDirectory = os.path.join(self.shared_folder, 'Results')
        outputFile = os.path.join(self.shared_folder, outputDirectory, 'index.html')
        
        returned_dict = run_lighter(input_file_info['files']['fwd'], outputFile, outputDirectory, params['kmer_params'], params['kmer_length'], params['genome_size'])
        logging.info('Returned dictionary: ' + str(returned_dict))


        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['input_reads_ref']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
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
