CREATE VIEW matchup_9 AS 
SELECT   
    reportype as reportype, 
    date,
    time,
    degrees(lat) as lat@hdr,
    degrees(lon) as lon@hdr,
    obsvalue@body,
    varno@body,
    entryno@body,
    fg_depar@body,
    datum_status@body as datum_status_hires@update_1,
    biascorr_fg,
    umod_old@satob,
    vmod_old@satob,
    vertco_reference_1@body
FROM hdr, body, satob
WHERE reportype is not null
AND groupid=9;

