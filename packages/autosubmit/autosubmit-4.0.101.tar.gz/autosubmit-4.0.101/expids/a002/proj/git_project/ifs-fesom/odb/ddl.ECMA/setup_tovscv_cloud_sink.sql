//
//-- ODB/SQL file 'setup_tovscv_cloud_sink.sql'
//
//   Last updated:  05-Jul-2002
//

READONLY;

CREATE VIEW setup_tovscv_cloud_sink AS
  SELECT seqno,timeslot,
         ctopbg,
         ctoper,
         ctop[1:$NMXUPD],
         camtbg,
         camter,
         camt[1:$NMXUPD],
   FROM  index, hdr, sat, radiance, cloud_sink
  WHERE  (obstype = $satem)
     AND (codetype = $atovs)
ORDERBY  timeslot, seqno
;
