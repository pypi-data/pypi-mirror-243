CREATE VIEW ralt  AS
SELECT  date, time, lat, lon, satellite_identifier@sat,
        obsvalue, fg_depar, an_depar,datastream,varno
FROM    hdr, body, sat
WHERE   obstype=12
  AND   varno IN (220, 221)
ORDERBY seqno
;

