READONLY;

SET $obstype = 0;
SET $codetype = 0;

CREATE VIEW fcq_robody_0 AS
SELECT 
   varno, datum_status@body, datum_event1@body, datum_anflag,     //  table body
   vertco_reference_1, vertco_reference_2, obsvalue, biascorr,
   level,mf_vertco_type,
FROM  index, hdr, conv, conv_body,body
WHERE  (obstype = $obstype) AND (codetype = $codetype)