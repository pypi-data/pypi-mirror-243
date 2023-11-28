
//
//-- ODB/SQL file 'satbody_atovs.sql'
//
//


SET $tslot = -1;
SET $kset = 0;

CREATE VIEW satbody_atovs_min AS    
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         emis_rtin READONLY, 
         emis_fg UPDATED,
         tausfc UPDATED,
         channel_qc READONLY,              // r/o                
  FROM   timeslot_index, index, hdr, body, radiance_body
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
    AND  obstype = $satem AND codetype = $atovs

 ORDERBY seqno
;
