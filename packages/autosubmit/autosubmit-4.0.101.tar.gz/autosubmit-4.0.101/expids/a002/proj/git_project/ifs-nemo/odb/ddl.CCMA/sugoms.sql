SET $tslot = -1;
//
// F. Duruisseau 26-sep-2018 add sensor
//
READONLY;

CREATE VIEW sugoms AS
  SELECT seqno, // for debugging purposes only
         timeslot@index, obstype, 
	       mapomm,
         sensor@hdr,
       areatype@hdr
    FROM timeslot_index, index, hdr
   WHERE ($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot)
 ORDERBY mapomm
;
