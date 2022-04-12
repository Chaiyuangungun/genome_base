import argparse
def get_genome_file(genome_file):
    chr = {}
    chr_long = {}
    with open(genome_file,"r") as f1:
        for line in f1:
            if ">" in line  :
                chr_num = line.strip().strip(">")
                chr[chr_num] = ""
                continue
            chr[chr_num] += line.strip()
    for chr_num in chr:
        print(chr_num+" : "+str(len(chr[chr_num])))

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("-genome", type=str)#基因组文件
args = parser.parse_args()
genome_file = args.genome 
get_genome_file(genome_file)
