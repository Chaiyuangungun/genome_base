import argparse

def get_genome_fasta(genome_file) :
    genome = {}
    with open(genome_file,"r") as f1:
        for line in f1:
            if ">" in line:
                chr = line.strip().strip(">")
                genome[chr] = ""
            else:
                genome[chr] += line.strip()
    return genome
def get_gene_gff(gene_id_file,gff_file) :
    gene_ids = []
    gene_gff = {}
    with open(gene_id_file,"r") as f1:
        for line in f1:
            gene_ids.append(line.strip())
    with open(gff_file,"r") as f2:
        for line in f2:
            if "gene" in line and line[:3] == "Chr":
                lines = line.strip().split()
                Chr = lines[0]
                start = lines[3]
                end = lines[4]
                direction = lines[6]
                id = lines[-1].split(";")[0].replace("ID=","")
                gene_gff[id] = [Chr,start,end,direction]
    return gene_ids,gene_gff
def get_gene_promoter(genome,gene_ids,gene_gff,promoter_num):
    promoter_fasta = {}
    num = int(promoter_num)
    for gene_id in gene_ids:
        Chrs = gene_gff[gene_id][0]
        start = int(gene_gff[gene_id][1])
        end = int(gene_gff[gene_id][2])
        dircetion = gene_gff[gene_id][3]
        if dircetion == "+":
            promoter_fasta[gene_id] = genome[Chrs][start-2000:start]
        elif dircetion == "-":
            promoter_fasta[gene_id] = genome[Chrs][end:end+2000][::-1].replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper()
    return promoter_fasta
def write_fasta_file(promoter_fasta,out_file):
    with open(out_file,"w") as f1:
        for gene_id in promoter_fasta:
            f1.write(">"+gene_id+"\n"+promoter_fasta[gene_id]+"\n")

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("-genome", type=str)#基因组文件
parser.add_argument("-gff", type=str)#gff文件
parser.add_argument("-id", type=str)#geneid文件
parser.add_argument("-nums", type=int,default=2000)#取起始位置上游多少bp
parser.add_argument("-out", type=str,default="out_file")#输出文件
args = parser.parse_args()

genome_file = args.genome 
gff_file = args.gff 
gene_id_file = args.id 
promoter_num = args.nums
out_file = args.out 
genome = get_genome_fasta(genome_file)
gene_ids,gene_gff = get_gene_gff(gene_id_file,gff_file)
promoter_fasta = get_gene_promoter(genome,gene_ids,gene_gff,promoter_num)
write_fasta_file(promoter_fasta,out_file)

