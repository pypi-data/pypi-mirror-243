import pandas as pd
pd.options.mode.chained_assignment = None
from tqdm import tqdm
import pandas as pd
import pkg_resources
import re
import requests
import tarfile
import platform
import os
from ftplib import FTP
pd.options.mode.chained_assignment = None
import warnings
import json
import subprocess

warnings.filterwarnings("ignore")


 #       _  ____   _         _____              _                      __ _____  __  
 #      | ||  _ \ (_)       / ____|            | |                    / /|  __ \ \ \ 
 #      | || |_) | _   ___ | (___   _   _  ___ | |_  ___  _ __ ___   | | | |__) | | |
 #  _   | ||  _ < | | / _ \ \___ \ | | | |/ __|| __|/ _ \| '_ ` _ \  | | |  _  /  | |
 # | |__| || |_) || || (_) |____) || |_| |\__ \| |_|  __/| | | | | | | | | | \ \  | |
 #  \____/ |____/ |_| \___/|_____/  \__, ||___/ \__|\___||_| |_| |_|  \_\|_|  \_\/_/
 #                                   __/ |                                   
 #                                  |___/      

#Geta data directory

def get_package_directory():
    return pkg_resources.resource_filename(__name__, '')


_cwd = str(get_package_directory())


# instalation def


def create_temporary_directory(source = None):
    if source == None:
        source = os.getcwd()
        
    if not os.path.exists(os.path.join(source, 'tmp')):
        os.makedirs(os.path.join(source, 'tmp'))
        
        

def download_and_prepare_UTRs(source = None, min_size = 50):
    
 
    
    import urllib
    import gzip
    import shutil
    
    if source == None:
        source = os.getcwd()
        
    url = 'http://srv00.recas.ba.infn.it/webshare/utrdb/Homo_sapiens.GRCh38.107.utrs.gz'

    local_filename = 'Homo_sapiens.GRCh38.107.utrs.gz'
    
    local_filename = os.path.join(source, local_filename)
    
    # Download 
    urllib.request.urlretrieve(url, local_filename)
    
    # Unzip 
    
    file_path = 'Homo_sapiens.GRCh38.107.utrs'
    
    file_path = os.path.join(source, file_path)
    
    with gzip.open(local_filename, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    

    
    def read_fasta(file_path):
     headers = []
     sequences = []
 
     with open(file_path, 'r') as fasta_file:
         current_header = None
         current_sequence = ""
 
         for line in fasta_file:
             line = line.strip()
 
             if line.startswith('>'):
                 if current_header is not None:
                     headers.append(current_header)
                     sequences.append(current_sequence)
                 current_header = line[1:]
                 current_sequence = ""
             else:
                 current_sequence += line
 
         if current_header is not None:
             headers.append(current_header)
             sequences.append(current_sequence)
 
     return headers, sequences

    header, sequence = read_fasta(file_path)
    
    gene = []
    ids = []
    utr = []
    location = []
    for sp in tqdm(header):
        split_elements = sp.split('|')
        gene.append(split_elements[3])
        ids.append(split_elements[2])
        utr.append(split_elements[1])
        location.append(split_elements[4])
        
    lengths = [len(x) for x in sequence]
    dict_fasta = pd.DataFrame({'gene':gene, 'id':ids, 'location':location, 'size':lengths, 'sequence':sequence})
    
    
    
    dict_fasta['gene'] = gene
    dict_fasta['ids'] = ids
    dict_fasta['utr'] = utr
    dict_fasta['location'] = location
    
    
    dict_fasta = dict_fasta[dict_fasta['size'] > min_size]
    
    
    utr3 = dict_fasta[dict_fasta['utr'] == 'three_prime_utr']
    
    utr3['utr'] = '3`UTR'
    
    utr5 = dict_fasta[dict_fasta['utr'] == 'five_prime_utr']
    
    utr5['utr'] = '5`UTR'
    
    del dict_fasta

    
   
   
    
    tata_box_pos = []
    tata_box__n = []

    tata_box_pattern = re.compile(r'TATA[AT]A[AT]')
    for seq in tqdm(utr5['sequence']):
        matches = tata_box_pattern.finditer(seq)
        tata_box_positions = [[match.start(), match.end()] for match in matches]
        if len(tata_box_positions) > 0:
            tata_box_pos.append(tata_box_positions)
            tata_box__n.append(len(tata_box_positions))
        else:
            tata_box_pos.append(None)
            tata_box__n.append(0)

     
    gc_box_pos = []
    gc_box_n = []

    gc_box_pattern = re.compile(r'GGGCGG')
    for seq in tqdm(utr5['sequence']):
        matches = gc_box_pattern.finditer(seq)
        gc_box_positions = [[match.start(), match.end()] for match in matches]
        if len(gc_box_positions) > 0:
            gc_box_pos.append(gc_box_positions)
            gc_box_n.append(len(gc_box_positions))

        else:
            gc_box_pos.append(None)
            gc_box_n.append(0)

            
    
    
    def find_orfs(sequence):
        start_codon = "ATG"
        stop_codons = ["TAA", "TAG", "TGA"]
        
        orf_positions = []
        
        i = 0
        while i < len(sequence):
            start_index = sequence.find(start_codon, i)
        
            if start_index == -1:
                break  
        
            stop_indices = [
                sequence.find(stop_codon, start_index) for stop_codon in stop_codons
                if sequence.find(stop_codon, start_index) != -1
            ]
        
            if any(stop_indices):  
                stop_index = min(stop_indices)
            else:
                break  
        
            orf_positions.append((start_index, stop_index + 3))
        
            i = stop_index + 3
        
        return orf_positions

    
    uorf_position = []
    uorf_n = []
    for seq in tqdm(utr5['sequence']):
        orfs = find_orfs(seq)
        if len(orfs) > 0:
            uorf_position.append(orfs)
            uorf_n.append(len(orfs))
        else:
            uorf_position.append(None)
            uorf_n.append(0)

    
    gc = []
    at = []
    for seq in tqdm(utr5['sequence']):
        gc.append(round((seq.count('G') + seq.count('C')) / len(seq) * 100, 2))
        at.append(round((seq.count('A') + seq.count('T')) / len(seq) * 100, 2))

         
    utr5['GC_box'] = gc_box_n
    utr5['TATA_box'] = tata_box__n
    utr5['uORFs'] = uorf_n
    utr5['AT%'] = at
    utr5['GC%'] = gc

    

         
    utr5['GC_box_position'] = gc_box_pos
    utr5['TATA_box_position'] = tata_box_pos
    utr5['uORF_position'] = uorf_position

    
    polyA_signal_pos = []
    polyA_signal_n = []

    polyA_signal_pattern = re.compile(r'AATAAA')
    for seq in tqdm(utr3['sequence']):
        matches = polyA_signal_pattern.finditer(seq)
        polyA_signal_positions = [[match.start(), match.end()] for match in matches]
        if len(polyA_signal_positions) > 0:
            polyA_signal_pos.append(polyA_signal_positions)
            polyA_signal_n.append(len(polyA_signal_positions))

        else:
            polyA_signal_pos.append(None)
            polyA_signal_n.append(0)
            
            
    utr3['polyA_signal_n'] = polyA_signal_n
    
    gc = []
    at = []
    for seq in tqdm(utr3['sequence']):
        gc.append(round((seq.count('G') + seq.count('C')) / len(seq) * 100, 2))
        at.append(round((seq.count('A') + seq.count('T')) / len(seq) * 100, 2))
        
        
    utr3['AT%'] = at
    utr3['GC%'] = gc
    utr3['polyA_signal_position'] = polyA_signal_pos
    
    
    
        
    try:
        os.remove(file_path)
        print(f'{file_path} successfully deleted.')
    except OSError as e:
        print(f'Error: {file_path} - {e.strerror}')
        
        
        
    try:
        os.remove(local_filename)
        print(f'{local_filename} successfully deleted.')
    except OSError as e:
        print(f'Error: {local_filename} - {e.strerror}')
    
    
        

    
    return utr5, utr3
    




def install_muscle(source = None):

    windows = 'https://drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86win32.exe'
    linux = 'https://drive5.com/muscle/muscle_src_3.8.1551.tar.gz'
    
    
    system = platform.system()
    
    if source == None:
        source = os.getcwd()
        
    if not os.path.exists(os.path.join(source, 'muscle')):
        os.makedirs(os.path.join(source, 'muscle'))
    
    if system == "Windows":
        print("\nWindows operating system")
        muscle_executable = os.path.join(source, 'muscle/windows/muscle3.8.31_i86win32.exe')
        
        if not os.path.exists(os.path.join(source, 'muscle/windows')):
            os.makedirs(os.path.join(source, 'muscle/windows'))

        
        # Download the file
        response = requests.get(windows)
        if response.status_code == 200:
            with open(muscle_executable, 'wb') as f:
                f.write(response.content)
        else:
            print(f"\nFailed to download the file. HTTP status code: {response.status_code}")
            exit(1)
        


    elif system == "Linux":
        print("\nLinux operating system")
        muscle_executable = os.path.join(source, 'muscle/linux/muscle_src_3.8.1551.tar.gz')
                
        if not os.path.exists(os.path.join(source, 'muscle/linux')):
            os.makedirs(os.path.join(source, 'muscle/linux'))

        
        # Download the file
        response = requests.get(linux)
        if response.status_code == 200:
            with open(muscle_executable, 'wb') as f:
                f.write(response.content)
        else:
            print(f"\nFailed to download the file. HTTP status code: {response.status_code}")
            exit(1)
            
        with tarfile.open(muscle_executable, 'r:gz') as tar:
            tar.extractall(path=os.path.join(source, 'muscle/linux/'))
            

        # Clean up: remove the downloaded archive file
        os.remove(muscle_executable)
        
        make_path=os.path.join(source, 'muscle/linux')
        
        command_list = ["make"]
    
        subprocess.run(command_list, cwd=make_path)

 

def install_blast(source = None):
    
    windows = 'https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.14.1/ncbi-blast-2.14.1+-x64-win64.tar.gz'
    linux = 'https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.14.1/ncbi-blast-2.14.1+-x64-linux.tar.gz'
    
    
    system = platform.system()
    
    if source == None:
        source = os.getcwd()
        
    if not os.path.exists(os.path.join(source, 'blast')):
        os.makedirs(os.path.join(source, 'blast'))
    
    if system == "Windows":
        print("\nWindows operating system")
        blast = os.path.join(source, 'blast/windows/ncbi-blast-2.14.1+-x64-win64.tar.gz')
        
        if not os.path.exists(os.path.join(source, 'blast/windows')):
            os.makedirs(os.path.join(source, 'blast/windows'))

        
        # Download the file
        response = requests.get(windows)
        if response.status_code == 200:
            with open(blast, 'wb') as f:
                f.write(response.content)
        else:
            print(f"\nFailed to download the file. HTTP status code: {response.status_code}")
            exit(1)
            
        with tarfile.open(blast, 'r:gz') as tar:
            tar.extractall(path=os.path.join(source, 'blast/windows/'))
            

        # Clean up: remove the downloaded archive file
        os.remove(blast)

    elif system == "Linux":
        print("\nLinux operating system")
        blast = os.path.join(source, 'blast/linux/ncbi-blast-2.14.1+-x64-linux.tar.gz')
        
        if not os.path.exists(os.path.join(source, 'blast/linux')):
            os.makedirs(os.path.join(source, 'blast/linux'))

        
        # Download the file
        response = requests.get(linux)
        if response.status_code == 200:
            with open(blast, 'wb') as f:
                f.write(response.content)
        else:
            print(f"\nFailed to download the file. HTTP status code: {response.status_code}")
            exit(1)
            
        with tarfile.open(blast, 'r:gz') as tar:
            tar.extractall(path=os.path.join(source, 'blast/linux/'))
            

        # Clean up: remove the downloaded archive file
        os.remove(blast)
 
        
 

def download_refseq_db(path_to_save = None, db = 'refseq_select_rna'):    

    if path_to_save == None:
        path_to_save = os.getcwd() 
        
    
    system = platform.system()
    
    
    if system == "Windows":
        print("\nWindows operating system")    
        path_to_save = os.path.join(path_to_save, 'blast/windows/ncbi-blast-2.14.1+/bin')
    
    
    elif system == "Linux":
        print("\nLinux operating system")        
        path_to_save = os.path.join(path_to_save, 'blast/linux/ncbi-blast-2.14.1+/bin')

    
    
    # Define the FTP URL and directory
    ftp_url = "ftp.ncbi.nlm.nih.gov"
    ftp_directory = "/blast/db/"
    
    # Connect to the FTP server
    ftp = FTP(ftp_url)
    ftp.login()
    
    # Change to the directory containing RefSeq RNA databases
    ftp.cwd(ftp_directory)
    
    # List the available files in the directory
    file_list = ftp.nlst()
    
    # Define the name of the RefSeq RNA database you want to download    
    
    file_list = [x for x in file_list if db in x and x.endswith('tar.gz') and not x.endswith('md5')]
    
    for file in tqdm(file_list):
        local_file_path = os.path.join(path_to_save, file)
    
        # Download the database file
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary('RETR ' + file, local_file.write)
            
        with tarfile.open(local_file_path, 'r:gz') as tar:
            tar.extractall(path=path_to_save)
            

        
        try:
            os.remove(local_file_path)
            print(f'{local_file_path} successfully deleted.')
        except OSError as e:
            print(f'Error: {local_file_path} - {e.strerror}')
        
            
        
        print(f"\n{db} has been downloaded to {local_file_path}")
    
    # Close the FTP connection
    ftp.quit()
    
  
    
  
    
#full instalation

def jseq_install(source = _cwd):
    
    """
    Installation function all dependencies of JBioSeqTools library
    
    Args:
       source: libbrary_working_directory    
    
    Returns:
        Full library installation
       
    """

    try:
        create_temporary_directory(source = source)
        install_muscle(source = source)
        install_blast(source = source)
        download_refseq_db(path_to_save = source, db = 'refseq_select_rna')
        
        utr5, utr3 = download_and_prepare_UTRs(source = source, min_size = 50)
          
        utr5 = utr5.to_dict(orient = 'list')
        
        file_path = 'data/utr5.json'
        file_path = os.path.join(source, file_path)
        
        with open(file_path, 'w') as json_file:
            json.dump(utr5, json_file)
            
        utr3 = utr3.to_dict(orient = 'list')
        
        file_path = 'data/utr3.json'
        file_path = os.path.join(source, file_path)
    
        
        with open(file_path, 'w') as json_file:
            json.dump(utr3, json_file)
            
    except:
        print('Trouble with first installation! Try again or contact us!')
        



 #       _  ____   _         _____              _                      __ _____  __  
 #      | ||  _ \ (_)       / ____|            | |                    / /|  __ \ \ \ 
 #      | || |_) | _   ___ | (___   _   _  ___ | |_  ___  _ __ ___   | | | |__) | | |
 #  _   | ||  _ < | | / _ \ \___ \ | | | |/ __|| __|/ _ \| '_ ` _ \  | | |  _  /  | |
 # | |__| || |_) || || (_) |____) || |_| |\__ \| |_|  __/| | | | | | | | | | \ \  | |
 #  \____/ |____/ |_| \___/|_____/  \__, ||___/ \__|\___||_| |_| |_|  \_\|_|  \_\/_/
 #                                   __/ |                                   
 #                                  |___/      
    
    