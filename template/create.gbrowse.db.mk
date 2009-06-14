moa_ids += create.gbrowse.db

#create.gbrowse.db_help = Create a gbrowse database
moa_title_create.gbrowse.db = Create a gbrowse database
moa_description_create.gbrowse.db = Create a gbrowse database
moa_must_define += gbrowse_user gbrowse_db
gbrowse_user_help = gbrowse db user
gbrowse_db_help = gbrowse db

include $(shell echo $$MOABASE)/template/moaBase.mk

.PHONY: create.gbrowse.db_prepare
create.gbrowse.db_prepare:

create.gbrowse.db:
	bp_seqfeature_load.pl -d $(gbrowse_db) -u $(gbrowse_user) -c
	touch create.gbrowse.db

.PHONY: create.gbrowse.db_post
create.gbrowse.db_post:

.PHONY: create.gbrowse.db_clean
create.gbrowse.db_clean:
	bp_seqfeature_load.pl -d $(gbrowse_db) -u $(gbrowse_user) -c
