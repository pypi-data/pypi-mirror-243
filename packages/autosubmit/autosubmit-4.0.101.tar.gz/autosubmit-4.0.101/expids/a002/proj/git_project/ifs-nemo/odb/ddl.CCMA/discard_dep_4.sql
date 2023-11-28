//
//-- ODB/SQL file 'discard_dep_4.sql'
//
//   Last updated:   28-Aug-2001
//

UPDATED;

SET $tslot = -1;

CREATE VIEW discard_dep_4 AS
  SELECT hires,    // Updated
	 lores,    // Updated
  FROM   index, hdr, update[min(4,$nmxupd)] 
  WHERE	 timeslot = $tslot OR $tslot = -1
;
