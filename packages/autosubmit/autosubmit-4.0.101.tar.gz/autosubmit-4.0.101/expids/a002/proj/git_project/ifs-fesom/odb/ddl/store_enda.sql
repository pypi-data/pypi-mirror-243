//
//-- ODB/SQL file 'store_enda.sql'
//
//   Last updated:  15/06/12
//   By          :  Anne Fouilloux

READONLY;

CREATE VIEW store_enda AS
  SELECT
    report_status, 
    report_event1,
    obsvalue,
    datum_anflag,
    datum_status,
    datum_event1,
    biascorr,
    biascorr_fg,
    an_depar,
    fg_depar,
    qc_pge,
    obs_error,
    final_obs_error,
    fg_error, 
    FROM   hdr, body, errstat
;

