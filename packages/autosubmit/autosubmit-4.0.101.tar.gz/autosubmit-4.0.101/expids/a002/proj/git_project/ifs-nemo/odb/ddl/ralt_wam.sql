//
//-- ODB/SQL file 'ralt_wam.sql'
//
//   Last updated:  10-Feb-2015
//

CREATE VIEW ralt_wam AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         obstype,                      // r/o
         codetype,                     // r/o
         date,                         // r/o
         time,                         // r/o
         varno,                        // r/o
         obsvalue,                     // r/o
         biascorr,                     // r/o
         obs_error,                    // r/o
         satellite_identifier,         // r/o
         fg_depar,                     // possibly updated
         an_depar,                     // possibly updated
         gp_number,                    // r/o
         report_status,
         report_event1,
         report_event2,
         datum_status,
         datum_event1,
         datum_event2,
         distribtype,                  // type of distribution - default is 0 i.e. no redistribution
         sensor@hdr,
  FROM   hdr, sat, body, errstat
  WHERE         obstype = $ralt
;
