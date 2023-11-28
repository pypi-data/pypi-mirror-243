CREATE VIEW matchup_17 AS
SELECT   
    reportype as reportype,
    date@hdr,
    time@hdr,
    degrees(lat@hdr) as lat@hdr,
    degrees(lon@hdr) as lon@hdr,
    obsvalue@body,
    varno@body,
    entryno@body,
    fg_depar@body,
    datum_status@body as datum_status_hires@update_1,
    biascorr_fg@body,
    an_depar@surfbody_feedback,
    fg_depar@surfbody_feedback,
    snow_depth@surfbody_feedback,
    snow_density@surfbody_feedback,
    datum_status@surfbody_feedback,
    datum_sfc_event@surfbody_feedback,
    lsm@surfbody_feedback
FROM hdr, body, surfbody_feedback
WHERE reportype is not null
AND groupid=17;
