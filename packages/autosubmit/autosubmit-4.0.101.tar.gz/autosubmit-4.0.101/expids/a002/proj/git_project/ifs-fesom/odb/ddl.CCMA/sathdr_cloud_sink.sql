//
//-- ODB/SQL file 'sathdr_cloud_sink.sql'
//
//   Last updated:  07-Nov-2002
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sathdr_cloud_sink AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         ctopbg,
         ctoper,
         ctopinc,
         ctop[1:$NMXUPD],
         camtbg,
         camter,
         camtinc,
         camt[1:$NMXUPD],
    FROM timeslot_index, index, hdr, sat, radiance, cloud_sink
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $satem 
     AND codetype = $atovs
 ORDERBY seqno
;
