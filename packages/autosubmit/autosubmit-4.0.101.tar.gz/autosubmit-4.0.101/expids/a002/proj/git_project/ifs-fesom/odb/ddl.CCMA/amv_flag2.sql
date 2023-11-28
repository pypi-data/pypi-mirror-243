CREATE VIEW amv_flag2 AS
SELECT  datum_status.active@body, datum_status.passive@body,
        datum_status.rejected@body,datum_status.blacklisted@body,
        datum_event1.rdb_rejected@body,datum_event1.datum_redundant@body,
        datum_event1.level_redundant@body,datum_event1.duplicate@body,
        report_event1.redundant@hdr,datum_anflag.varqc@body,datum_anflag.fg@body,
        datum_event1.vertco_consistency@body,seqno
FROM    hdr, body
WHERE   obstype=$satob 
  AND   varno IN ($u)
ORDERBY seqno
;
