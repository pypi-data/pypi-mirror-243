//
//-- ODB/SQL file 'scat_ambig_select.sql'
//
//   Last updated:  19/02/2018 M.Hamrud Creation
//
// 
READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW scat_ambig_select AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         entryno READONLY,
         varno,
         obsvalue,
         ambig_select UPDATED,
  FROM   timeslot_index, index, hdr, body, scatt_body
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
   ORDERBY seqno
;
