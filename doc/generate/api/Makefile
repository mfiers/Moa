
all:
	-mkdir  $(MOABASE)/doc/api/images 
	cp ../../images/shadow.png $(MOABASE)/doc/api/images
	cp ../../images/moa_logo_pfr_header.png  $(MOABASE)/doc/api/images
	epydoc -vo $(MOABASE)/doc/api \
		$(MOABASE)/bin/moa \
	    $(MOABASE)/lib/python/moa/*py \
		$(MOABASE)/lib/python/moa/plugins/*py \
		-u http://mfiers.github.com/Moa/ \
		--css moaapi.css \
		--name "Moa" --no-frames
