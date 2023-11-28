CREATE VIEW tcwv AS
SELECT
date, time, satellite_identifier@sat,
lat, lon, lsm, obsvalue, fg_depar, an_depar, biascorr,
datum_status.active@body, datum_status.passive@body,
datum_status.rejected@body, datum_status.blacklisted@body,
datum_event1.rdb_rejected@body, datum_event1.datum_redundant@body,
datum_event1.level_redundant@body,
datum_event1.duplicate@body, report_event1.redundant@hdr,
datum_anflag.varqc@body, datum_anflag.fg@body

FROM hdr, body, sat, modsurf
WHERE
obstype@hdr=7 AND codetype=214 AND varno@body=9 AND fg_depar is not NULL
;
