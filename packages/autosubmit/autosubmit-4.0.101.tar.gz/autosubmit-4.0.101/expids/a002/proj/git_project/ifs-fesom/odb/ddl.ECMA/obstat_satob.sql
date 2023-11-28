READONLY;

SET $use_twindow = 0;
SET $refdate=0; // Reference date (OBSTAT_BASEDATE's yyyymmdd)
SET $reftime=0; // Reference time (OBSTAT_BASEDATE's hhmmss)
SET $refdt_l=0; // Left delta margin  (usually : - OBSTAT_TSTEP/2 + 1 minute)
SET $refdt_r=0; // Right delta margin (usually : + OBSTAT_TSTEP/2 ... exact)

SET $body_min =  1;
SET $body_max = -1;

CREATE VIEW obstat_satob AS 
SELECT
// --------- Real part of sql request -------------
   varno, lat, lon, lsm, vertco_reference_1,
//   1     2    3     4
  obsvalue, fg_depar, an_depar, obs_error, fg_error,
//   5        6          7          8         9
  hires@update_2,
//   10              11               12
  qc_pge, qc_l, biascorr, statid, biascorr_fg,
//   13          14         15        16      17
  qi_fc@satob, qi_nofc@satob,
//   18           19
// --------- Integer part of sql request -------------
  codetype, obstype, subtype, sensor,datastream@sat, time, date,
//   20       21     22             23    24
  datum_status@body, report_status@hdr, report_event1@hdr, report_rdbflag@hdr,
//    25          26          27          28
  datum_anflag, datum_event1@body
//   29        30
// --------- Auxiliary part of sql request (only used in odbread.F90)
FROM hdr, modsurf, body, update_2, errstat, satob, sat
WHERE (($body_max == -1) OR
       (#body BETWEEN $body_min AND $body_max))   // delta-rows is $OBSTAT_BODY_CHUNK
      AND
      (( $use_twindow = 0) OR
       ( $use_twindow > 0 AND
         twindow(date,time,$refdate,$reftime,$refdt_l,$refdt_r)))
;

