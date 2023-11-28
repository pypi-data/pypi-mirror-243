CREATE VIEW scatt AS
SELECT  date, time, lat, lon, satellite_identifier@sat,
        obsvalue, fg_depar, an_depar,datastream,varno
FROM    hdr, body, sat
WHERE   obstype=9 
  AND   varno IN (124, 125)
ORDERBY seqno
;

