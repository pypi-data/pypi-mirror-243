CREATE VIEW emiskf_mhs AS
  SELECT
    satellite_identifier@sat,
    vertco_reference_1@body,
    date@hdr,
    time@hdr,
    lldegrees(lon@hdr),
    lldegrees(lat@hdr),
    scanpos@radiance,
    emis_retr,
    zenith,
    fg_depar@body,
    sensor
  FROM hdr,sat,radiance, modsurf, body, radiance_body
  WHERE
    sensor == 15
    AND vertco_reference_1@body == 1
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
