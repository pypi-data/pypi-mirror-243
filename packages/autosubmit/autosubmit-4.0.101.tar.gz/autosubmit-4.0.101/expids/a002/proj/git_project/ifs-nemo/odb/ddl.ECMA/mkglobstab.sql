//
//-- ODB/SQL file 'mkglobstab.sql'
//
// F. Duruisseau 26-sep-2018 add sensor

CREATE VIEW mkglobstab AS
  SELECT seqno READONLY,
         timeslot READONLY,
         obstype READONLY,
         codetype READONLY,
         instrument_type READONLY,
         retrtype READONLY,
         areatype READONLY,
	       abnob READONLY, 
         mapomm,
         lat READONLY, 
         lon READONLY, 
         trlat READONLY,
         trlon READONLY,
         sensor@hdr,
    FROM index, hdr
 ORDERBY timeslot, seqno
;
