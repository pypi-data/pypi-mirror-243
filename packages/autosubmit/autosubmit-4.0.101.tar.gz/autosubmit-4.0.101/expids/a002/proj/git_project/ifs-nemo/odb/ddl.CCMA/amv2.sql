CREATE VIEW amv2 AS
SELECT  date, time, lat, lon, satellite_identifier@sat, comp_method, qi_fc, vertco_reference_1,
        obsvalue, fg_depar, an_depar, u_old, v_old, qi_nofc,datastream,
        seqno
FROM    hdr, body, sat, satob
WHERE   obstype=$satob 
  AND   varno IN ($u, $v)
ORDERBY seqno
;

