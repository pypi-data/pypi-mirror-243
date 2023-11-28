READONLY;

CREATE VIEW fcq_robody_2 AS
SELECT 
   varno, datum_status@body, datum_anflag,                    //  table body
   vertco_reference_2, obsvalue, biascorr,
FROM  index, hdr, body
WHERE  (obstype = $synop)
 AND   ((codetype = 21) OR (codetype = 24))
