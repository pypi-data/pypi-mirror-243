CREATE VIEW airs AS
SELECT 
lat, lon, body.len,
solar_zenith@sat, scanpos@radiance, time, lsm, date, 
vertco_reference_1, obsvalue, fg_depar, an_depar, lores@update_1,
biascorr, seqno
FROM
hdr, body, sat, radiance, modsurf, update_1
WHERE
obstype=7 AND satellite_identifier@sat=784
ORDERBY seqno
;

