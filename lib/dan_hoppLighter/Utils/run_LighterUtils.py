import subprocess
import os

# This will contain functions to run Lighter command line tool
def run_lighter(input_file, output_file, output_dir, kmer_size, genome_size, threads):
    try:
        # Construct the Lighter command with additional parameters
        command = [
            'lighter',
            '-r', input_file,
            '-od', output_dir,
            '-K', str(kmer_size),
            str(genome_size),
            '-t', str(threads)
        ]
        
        # Run the Lighter command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Write the output to the specified HTML-formatted file
        with open(output_file, 'w') as f:
            f.write("<html><body><pre>")
            f.write(result.stderr)
            f.write("</pre></body></html>")
            
        print(f"Lighter command executed successfully. Output saved to {output_file}\n")

        # Get the file name's prefix to the left of the . from input_file. Ignore the path.
        prefix = input_file.split('/')[-1].split('.')[0]

        # Return in a dictionary two file names found in the output_dir folder: The first has a .html prefix and the second has '.cor.' in the name and its filename prefix is the same as the input file's prefix.
        return {
            'console_output_file': output_file,
            'corrected_file': output_dir + '/' + [f for f in os.listdir(output_dir) if prefix in f][0]
        }

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Lighter: {e}")

# Example usage
# run_lighter('/kb/module/work/tmp/461665ae-f152-40f1-9c9c-55bf181a4d8b.single.fastq', 'output.txt', './Results', 17, 5000000, 10)