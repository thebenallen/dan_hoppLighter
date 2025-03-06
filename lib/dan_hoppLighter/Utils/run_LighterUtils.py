import subprocess
import os
from installed_clients.readsutilsClient import ReadsUtils
from installed_clients.DataFileUtilClient import DataFileUtil

def run_lighter(input_file, result_dir, report_file, kmer_size, genome_size, threads=10):
    try:
        # Construct the Lighter command with additional parameters
        command = [
            'lighter',
            '-r', input_file,
            '-od', result_dir,
            '-K', str(kmer_size),
            str(genome_size),
            '-t', str(threads)
        ]
        
        # Run the Lighter command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Create a directory for report_file if it doesn't exist
        if not os.path.exists(os.path.dirname(report_file)):
            os.makedirs(os.path.dirname(report_file))

        # Write the output to the specified HTML-formatted file
        with open(report_file, 'w') as f:
            f.write("<html><body><pre>")
            f.write(result.stderr)
            f.write("</pre></body></html>")
            
        print(f"Lighter command executed successfully. Output saved to {report_file}\n")

        # Get the file name's prefix to the left of the . from input_file. Ignore the path.
        prefix = input_file.split('/')[-1].split('.')[0]
        # extension = input_file.split('/')[-1].split('.')[1]

        # Return in a dictionary two file names found in the result_dir folder: The first has a .html prefix and the second has '.cor.' in the name and its filename prefix is the same as the input file's prefix.
        return {
            # 'console_report_file': report_file, # No need to return - input parameter is not altered.
            'corrected_file_path': result_dir + '/' + [f for f in os.listdir(result_dir) if prefix in f][0],
            'corrected_file_name': [f for f in os.listdir(result_dir) if prefix in f][0]
        }

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Lighter: {e}")


def upload_reads(callback_url, reads_file, ws_name, reads_obj_name, source_reads_upa):
    """
    callback_url = as usual.
    reads_file = full path to the reads file to upload
    ws_name = the workspace to use for uploading the reads file
    reads_obj_name = the name of the new reads object to save as
    source_reads = if not None, the source UPA for the original reads file.
    """
    # unfortunately, the ReadsUtils only accepts uncompressed fq files- this should
    # be fixed on the KBase side
    dfu = DataFileUtil(callback_url)
    reads_unpacked = dfu.unpack_file({'file_path': reads_file})['file_path']

    ru = ReadsUtils(callback_url)
    new_reads_upa = ru.upload_reads({
        'fwd_file': reads_unpacked,
        'interleaved': 1,
        'wsname': ws_name,
        'name': reads_obj_name,
        'source_reads_ref': source_reads_upa
    })['obj_ref']
    print('saved ' + str(reads_unpacked) + ' to ' + str(new_reads_upa))
    return new_reads_upa

"""
# This will contain functions to run Lighter command line tool
def run_lighter(input_files, report_file, result_dir, kmer_params, kmer_length, genome_size, alpha=None, threads=10, maxcor=4, trim=False, discard=False, noQual=False, newQual=None, saveTrustedKmers=None, loadTrustedKmers=None, zlib=None):
    try:
        # Construct the Lighter command with additional parameters
        command = [
            'lighter',
            '-od', result_dir,
            '-t', str(threads),
            '-maxcor', str(maxcor)
        ]
        
        # Add multiple input files
        for input_file in input_files:
            command.extend(['-r', input_file])
        
        if kmer_params == '-k':
            command.extend([kmer_params, str(kmer_length), str(genome_size), str(alpha)])
        elif kmer_params == '-K':
            command.extend([kmer_params, str(kmer_length), str(genome_size)])
        
        if trim:
            command.append('-trim')
        if discard:
            command.append('-discard')
        if noQual:
            command.append('-noQual')
        if newQual is not None:
            command.extend(['-newQual', str(newQual)])
        if saveTrustedKmers is not None:
            command.extend(['-saveTrustedKmers', saveTrustedKmers])
        if loadTrustedKmers is not None:
            command.extend(['-loadTrustedKmers', loadTrustedKmers])
        if zlib is not None:
            command.extend(['-zlib', str(zlib)])
        
        # Run the Lighter command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Write the output to the specified HTML-formatted file
        with open(report_file, 'w') as f:
            f.write("<html><body><pre>")
            f.write(result.stderr)
            f.write("</pre></body></html>")
            
        print(f"Lighter command executed successfully. Output saved to {report_file}\n")

        # Get the file name's prefixes to the left of the . from the input files. Ignore the path.
        prefixes = [input_file.split('/')[-1].split('.')[0] for input_file in input_files]

        # Return in a dictionary two file names found in the result_dir folder: The first has a .html prefix and the second has '.cor.' in the name and its filename prefix is the same as the input file's prefix.
        corrected_files = [result_dir + '/' + f for f in os.listdir(result_dir) if any(prefix in f for prefix in prefixes)]

        return {
            'console_report_file': report_file,
            'corrected_files': corrected_files
        }

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Lighter: {e}")
        """

# Example usage
# run_lighter('/kb/module/work/tmp/461665ae-f152-40f1-9c9c-55bf181a4d8b.single.fastq', 'output.txt', './Results', 17, 5000000, 10)