lftp_url=ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_bacteria.dat.gz
lftp_mode=get
lftp_timestamp=F
jid=moa_lftp_10.swissprot.bacteria_3d19591c95ab
g_input_dir=.
g_input_pattern=*.gz
g_name_sed=s/.dat.gz//
g_process=zcat $< | seqret swissprot::stdin fasta:$(g_target)
