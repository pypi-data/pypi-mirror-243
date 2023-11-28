//
//   Blacklisting default body query 
//
//   == ALWAYS keep black*1.sql to black*10.sql consistent! ==
//

READONLY; // Except entries those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW black_robody_7 AS
  SELECT seqno, // BLACKLIST CORE BODY START. SEQNO MUST COME FIRST
         entryno,
         datum_status@body     UPDATED, 
         datum_blacklist@body  UPDATED,
         datum_anflag          UPDATED,
         vertco_type,
         varno,
         vertco_reference_1,
         vertco_reference_2,
         obsvalue,
         fg_depar,
         final_obs_error,
         fg_error, // BLACKLIST CORE BODY END
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE	 (obstype = $satem)
    AND  (codetype = $resat)
    AND  (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
