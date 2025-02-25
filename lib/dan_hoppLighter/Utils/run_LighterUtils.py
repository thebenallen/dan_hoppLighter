import subprocess
import os

# This will contain functions to run Lighter command line tool
def run_lighter(input_files, output_file, output_dir, kmer_params, kmer_length, genome_size, alpha=None, threads=10, maxcor=4, trim=False, discard=False, noQual=False, newQual=None, saveTrustedKmers=None, loadTrustedKmers=None, zlib=None):
    try:
        # Construct the Lighter command with additional parameters
        command = [
            'lighter',
            '-od', output_dir,
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
        with open(output_file, 'w') as f:
            f.write("<html><body><pre>")
            f.write(result.stderr)
            f.write("</pre></body></html>")
            
        print(f"Lighter command executed successfully. Output saved to {output_file}\n")

        # Get the file name's prefixes to the left of the . from the input files. Ignore the path.
        prefixes = [input_file.split('/')[-1].split('.')[0] for input_file in input_files]

        # Return in a dictionary two file names found in the output_dir folder: The first has a .html prefix and the second has '.cor.' in the name and its filename prefix is the same as the input file's prefix.
        corrected_files = [output_dir + '/' + f for f in os.listdir(output_dir) if any(prefix in f for prefix in prefixes)]

        return {
            'console_output_file': output_file,
            'corrected_files': corrected_files
        }

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Lighter: {e}")

# Example usage
# run_lighter('/kb/module/work/tmp/461665ae-f152-40f1-9c9c-55bf181a4d8b.single.fastq', 'output.txt', './Results', 17, 5000000, 10)