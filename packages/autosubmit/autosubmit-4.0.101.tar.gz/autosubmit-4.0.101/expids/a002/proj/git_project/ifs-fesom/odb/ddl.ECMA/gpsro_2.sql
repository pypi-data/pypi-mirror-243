CREATE VIEW gpsro_2 AS
SELECT
date, time, satellite_identifier@sat, lat, lon, retrtype, radcurv@gnssro,
vertco_reference_1@body, obsvalue, fg_depar, an_depar, final_obs_error, biascorr,
datum_status.active@body, datum_status.passive@body,
datum_status.rejected@body, datum_status.blacklisted@body,
datum_event1.rdb_rejected@body, datum_event1.datum_redundant@body,
datum_event1.level_redundant@body,  datum_event1.duplicate@body,
report_event1.redundant@hdr, datum_anflag.varqc@body, datum_anflag.fg@body, seqno
FROM
index, hdr, body, errstat, sat, gnssro
WHERE
obsvalue is not NULL
ORDERBY seqno
;
