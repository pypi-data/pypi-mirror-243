SET $refdt_l=0;
SET $refdt_r=0;
SET $refdate=0;
SET $reftime=0;
SET $zatid  =-1;
SET $zenzor =-1;

CREATE VIEW amv AS
SELECT  date, time, lat, lon, satellite_identifier@sat, comp_method, qi_fc, vertco_reference_1,
        obsvalue, fg_depar, an_depar, u_old, v_old, seqno
FROM    hdr, body, sat, satob
WHERE   obstype=$satob 
  AND   satellite_identifier@sat = $zatid 
  AND   comp_method = $zenzor
  AND   twindow(date,time,$refdate,$reftime,$refdt_l,$refdt_r)
  AND   varno IN ($u, $v)
ORDERBY seqno
;
