CREATE VIEW gpsro AS
SELECT 
lat, lon, body.len, time, date, 
vertco_reference_1, obsvalue, fg_depar, an_depar, seqno
FROM
hdr, body, sat
WHERE
obstype=$limb
ORDERBY seqno
;

