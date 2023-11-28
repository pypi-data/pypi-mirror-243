READONLY;

SET $use_twindow = 0;
SET $refdate=0; // Reference date (OBSTAT_BASEDATE's yyyymmdd)
SET $reftime=0; // Reference time (OBSTAT_BASEDATE's hhmmss)
SET $refdt_l=0; // Left delta margin  (usually : - OBSTAT_TSTEP/2 + 1 minute)
SET $refdt_r=0; // Right delta margin (usually : + OBSTAT_TSTEP/2 ... exact)

SET $body_min =  1;
SET $body_max = -1;

CREATE VIEW obstat_mwimg AS 
SELECT
// --------- Real part of sql request -------------
   varno, lat, lon, lsm, vertco_reference_1,
//   1     2    3     4      5
  obsvalue, fg_depar, an_depar, obs_error, fg_error,
//   6        7          8          9         10
  hires@update_2, 
//   11              12               13
  qc_pge, qc_l, biascorr, statid, biascorr_fg, vertco_reference_2,
//   14          15         16        17      18        19
// --------- Integer part of sql request -------------
  codetype, obstype, subtype, sensor, time, date,
//   20      21       22   23
  datum_status@body, report_status@hdr, report_event1@hdr, report_rdbflag@hdr,
//     24          25          26         27
  datum_anflag, datum_event1@body, report_tbcloud
//   28          29      30
// --------- Auxiliary part of sql request (only used in odbread.F90)
FROM hdr, modsurf, body, update_2, errstat, sat, allsky
WHERE (($body_max == -1) OR
       (#body BETWEEN $body_min AND $body_max))   // delta-rows is $OBSTAT_BODY_CHUNK
      AND
      (( $use_twindow = 0) OR
       ( $use_twindow > 0 AND
         twindow(date,time,$refdate,$reftime,$refdt_l,$refdt_r)))
;

