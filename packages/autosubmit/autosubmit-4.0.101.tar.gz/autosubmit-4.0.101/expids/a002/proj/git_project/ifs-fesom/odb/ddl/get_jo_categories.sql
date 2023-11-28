READONLY; 

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW get_jo_categories AS
  SELECT seqno,
         entryno,
         varno,
         codetype,
         fg_error,
         final_obs_error
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
   ORDERBY seqno
;

