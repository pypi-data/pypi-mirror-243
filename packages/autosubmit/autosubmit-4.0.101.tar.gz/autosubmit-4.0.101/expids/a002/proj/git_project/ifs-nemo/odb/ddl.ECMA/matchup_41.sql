CREATE VIEW matchup_41 AS
SELECT   
    reportype as reportype,
    date,
    time,
    degrees(lat) as lat@hdr,
    degrees(lon) as lon@hdr,
    obsvalue@body,
    varno@body,
    entryno@body,
    datum_status@body as datum_status_hires@update_1,
    biascorr_fg
FROM hdr, body, surfbody_feedback
WHERE reportype is not null
AND groupid=41;
