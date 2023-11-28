READONLY;

SET $use_twindow = 0;
SET $refdate=0; // Reference date (OBSTAT_BASEDATE's yyyymmdd)
SET $reftime=0; // Reference time (OBSTAT_BASEDATE's hhmmss)
SET $refdt_l=0; // Left delta margin  (usually : - OBSTAT_TSTEP/2 + 1 minute)
SET $refdt_r=0; // Right delta margin (usually : + OBSTAT_TSTEP/2 ... exact)

SET $body_min =  1;
SET $body_max = -1;

CREATE VIEW obstat_radar AS 
SELECT
// --------- Real part of sql request -------------
   varno, lat, lon, vertco_reference_1@body,
//   1     2    3     4
  obsvalue, fg_depar, an_depar, obs_error, fg_error,
//   5        6          7          8         9   
  lores@update_1, hires@update_1, lores@update_2,
//   10              11               12
  qc_pge, qc_l, biascorr, statid, biascorr_fg,
//   13          14         15        16      17
  vertco_reference_2,
//   18
  elevation@radar_body, azimuth@radar_body, 
//   19      20
// --------- Integer part of sql request -------------
  codetype, satellite_identifier@sat, time@hdr, date, 
//   21      22      23    24  
  datum_status@body, report_status@hdr, report_event1@hdr, report_rdbflag@hdr,
//    25          26          27          28
  datum_anflag, datum_event1@body,
//   29        30    
// --------- Auxiliary part of sql request (only used in odbread.F90)
FROM index, hdr, sat, radar, radar_body, body, update_1,update_2, errstat
WHERE (($body_max == -1) OR
       (#body BETWEEN $body_min AND $body_max))   // delta-rows is $OBSTAT_BODY_CHUNK
      AND
      (( $use_twindow = 0) OR
       ( $use_twindow > 0 AND
         twindow(date,time@hdr,$refdate,$reftime,$refdt_l,$refdt_r)))
;
