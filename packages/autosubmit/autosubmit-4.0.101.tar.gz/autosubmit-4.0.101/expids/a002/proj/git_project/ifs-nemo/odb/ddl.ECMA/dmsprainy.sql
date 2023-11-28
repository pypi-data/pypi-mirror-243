CREATE VIEW dmsprainy AS
SELECT
date, time, satellite_identifier@sat, lat, lon, typesurf@radiance,
vertco_reference_1@body,obsvalue, rad_fg_depar@ssmi_body, rad_an_depar@ssmi_body, rad_bias@ssmi_body,
failure_1dvar, iterno_conv_1dvar,
datum_status.active@body, datum_status.passive@body,
datum_status.rejected@body, datum_status.blacklisted@body,
datum_event1.rdb_rejected@body, datum_event1.datum_redundant@body,
datum_event1.level_redundant@body,  datum_event1.duplicate@body,
report_event1.redundant@hdr, datum_anflag.varqc@body, datum_anflag.fg@body, seqno
FROM
hdr, body, sat, radiance, ssmi, ssmi_body
WHERE
obstype@hdr=7 AND codetype=215 AND varno@body=119
ORDERBY seqno
;
