CREATE VIEW gpsro_flag AS
SELECT  datum_status.active@body,       datum_status.passive@body,
        datum_status.rejected@body,     datum_status.blacklisted@body,
        datum_event1.rdb_rejected@body,     datum_event1.datum_redundant@body,
        datum_event1.level_redundant@body,  datum_event1.duplicate@body,
        report_event1.redundant@hdr,
	datum_anflag.varqc@body,        datum_anflag.fg@body,   seqno
FROM    
      hdr, body, sat
WHERE  
      obstype=$limb 
ORDERBY seqno
;

