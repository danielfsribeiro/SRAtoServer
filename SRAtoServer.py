#############################################################################################################
# Simple script to download SRA files with the SRA toolkit installed, and copy them to a server.

#
# Daniel Ribeiro 2022
#############################################################################################################
import subprocess
import argparse

def command_gen(commands:list) -> str:
    '''Generate a command fomr a list of arguments'''
    return " ".join(commands)

# Define arguments
parser = argparse.ArgumentParser(description="Simple Script to download SRA files with the SRA toolkit installed, and copy them to a server.\n",
                                 epilog="For --help on 'prefetch', use 'prefetch' command directly.")
parser.add_argument("-p", "--prefetch_progress", required=False, action="store_const", const= "-p", help="prefetch -p|--progress argument.\n")
#parser.add_argument("-C", "--prefetch_verify", required=False, help="prefetch -C|--verify argument <no|yes [defualt]>.\n", default="yes")
parser.add_argument("-a", "--accessions", required=True, help="A text file with accessions numbers, one per line.\n")
parser.add_argument("-l", "--local_dir", required=True, help="/path/to/sra/cache. Check '$vbd-config -i'.\n")
parser.add_argument("-r", "--remote_dir", required=True, help="/path/to/remote/server/dir. \n")
args = parser.parse_args()

# Check existance of 'prefetch' from SRA toolkint
result = subprocess.run("command -v prefetch", shell=True, capture_output=True, text=True)
if not result.stdout:
    print("'prefetch' not found! Is SRA Toolkit installed?")
    exit()

# Load accession list
f = open(args.accessions, mode='r')
for line in f:
    # Execute prefetch
    sra_file = line.strip()
    #prefetch_opt = command_gen([args.prefetch_progress, args.prefetch_verify])
    prefetch_opt = command_gen([args.prefetch_progress])
    command = command_gen(["prefetch", prefetch_opt, sra_file])
    print(f"\n***Excecute 'prefetch': {command}")
    subprocess.run(command, shell=True)
    # Copy to remote
    command = command_gen(["scp", args.local_dir + '/sra/' + sra_file + '.sra', args.remote_dir])
    print(f"\n***Excecute 'scp': {command}")
    subprocess.run(command, shell=True)
    # Cleanup local files
    command = command_gen(["rm", args.local_dir + '/sra/' + sra_file + '.sra'])
    print(f"\n***Excecute local 'rm': {command}")
    subprocess.run(command, shell=True)



