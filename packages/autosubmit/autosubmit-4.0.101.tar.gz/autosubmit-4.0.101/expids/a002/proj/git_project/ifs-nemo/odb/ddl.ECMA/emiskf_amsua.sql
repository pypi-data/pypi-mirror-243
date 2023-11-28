CREATE VIEW emiskf_amsua AS
  SELECT
    satellite_identifier@sat,
    vertco_reference_1,
    date,
    time,
    lldegrees(lon@hdr),
    lldegrees(lat@hdr),
    scanpos@radiance,
    emis_retr,
    zenith,
    fg_depar,
    sensor
  FROM hdr,sat,radiance, body, modsurf, radiance_body
  WHERE
    sensor@hdr == 3
    AND vertco_reference_1@body == 3
    AND emis_retr is not NULL
    AND emis_retr >= 0.45 and emis_retr <= 1.0
    AND fg_depar is not NULL
    AND zenith is not NULL
    AND datum_status.blacklisted@body == 1
    AND datum_status.use_emiskf_only@body == 1
    AND datum_event1.contam_cld_flag@body == 0
    AND lsm > 0.8
    AND datastream = 0
;
