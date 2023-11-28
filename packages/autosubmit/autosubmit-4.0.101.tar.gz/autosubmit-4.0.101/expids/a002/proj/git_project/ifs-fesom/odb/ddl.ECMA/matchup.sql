CREATE VIEW matchup AS
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
    biascorr_fg
FROM hdr, body
WHERE reportype is not null;
