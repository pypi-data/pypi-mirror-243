SET $refdt_l=0;
SET $refdt_r=0;
SET $refdate=0;
SET $reftime=0;
SET $zatid  =-1;
SET $zenzor =-1;

CREATE VIEW amv_flag AS
SELECT  datum_status.active@body, datum_status.passive@body,
        datum_status.rejected@body,datum_status.blacklisted@body,
        datum_event1.rdb_rejected@body,datum_event1.datum_redundant@body,
        datum_event1.level_redundant@body,datum_event1.duplicate@body,
        report_event1.redundant@hdr,datum_anflag.varqc@body,datum_anflag.fg@body,
        datum_event1.vertco_consistency@body,seqno
FROM    hdr, body, sat, satob
WHERE   obstype=$satob 
  AND   satellite_identifier@sat = $zatid 
  AND   comp_method = $zenzor
  AND   twindow(date,time,$refdate,$reftime,$refdt_l,$refdt_r)
  AND   varno IN ($u)
ORDERBY seqno
;
